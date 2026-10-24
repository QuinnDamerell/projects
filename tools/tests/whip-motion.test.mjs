import assert from 'node:assert/strict';
import test from 'node:test';
import { screenTilt, createGestureTracker, SWING_DEGREES } from '../../docs/javascripts/whip-app.js';

const radians = Math.PI / 180;
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const wrap = (value, low) => ((value - low) % 360 + 360) % 360 + low;
const mix = (a, b, s, c) => a.map((value, index) => value * s + b[index] * c);

// Legal W3C Z-X'-Y'' angles for a phone whose top and screen point along the
// given world vectors (x east, y north, z up), as a browser would report them.
function reading(top, screen) {
  const right = cross(top, screen);
  const m = [[right[0], top[0], screen[0]], [right[1], top[1], screen[1]], [right[2], top[2], screen[2]]];
  const flipped = m[2][2] < 0;
  let beta = flipped ? Math.PI - Math.asin(m[2][1]) : Math.asin(m[2][1]);
  let gamma = flipped ? Math.atan2(m[2][0], -m[2][2]) : Math.atan2(-m[2][0], m[2][2]);
  let alpha = flipped ? Math.atan2(m[0][1], -m[1][1]) : Math.atan2(-m[0][1], m[1][1]);
  if (Math.abs(Math.cos(beta)) < 1e-9) {
    gamma = 0;
    alpha = Math.atan2(m[1][0], m[0][0]);
  }
  return { alpha: wrap(alpha / radians, 0), beta: wrap(beta / radians, -180), gamma: gamma / radians };
}

// The player faces `heading` degrees clockwise from north and looks at the
// screen, which leans back by `pitch` (0 upright, 90 lying flat). `tilt` turns
// the phone in its screen plane like a steering wheel: negative moves the top
// toward the screen's left edge (the Whip diagram), positive toward its right.
function pose(tilt, { pitch = 0, heading = 0 } = {}) {
  const forward = [Math.sin(heading * radians), Math.cos(heading * radians), 0];
  const right = [Math.cos(heading * radians), -Math.sin(heading * radians), 0];
  const up = [0, 0, 1];
  const upright = mix(forward, up, Math.sin(pitch * radians), Math.cos(pitch * radians));
  const screen = mix(forward, up, -Math.cos(pitch * radians), Math.sin(pitch * radians));
  const top = mix(upright, right, Math.cos(tilt * radians), Math.sin(tilt * radians));
  return reading(top, screen);
}

function play(tracker, readings) {
  return readings.map(event => tracker.sample(event).sound);
}

function sweep(from, to, step) {
  const values = [];
  for (let value = from; step > 0 ? value <= to : value >= to; value += step) values.push(value);
  return values;
}

test('screen tilt is the steering-wheel angle at any heading or lean', () => {
  for (const heading of [0, 90, 200]) {
    for (const pitch of [-30, 0, 30, 60]) {
      for (const tilt of [-170, -100, -45, 0, 45, 100, 170]) {
        const measured = screenTilt(pose(tilt, { pitch, heading })).tilt;
        assert.ok(Math.abs(measured - tilt) < 1e-9, `${heading} ${pitch} ${tilt}: ${measured}`);
      }
    }
  }
});

test('only gravity matters, so a missing heading is fine and bad angles are rejected', () => {
  const level = event => assert.ok(Math.abs(screenTilt(event).tilt) < 1e-9, JSON.stringify(event));
  level({ alpha: null, beta: 60, gamma: 0 });
  // Upright, browsers may report one attitude with alpha and gamma traded.
  level({ alpha: 0, beta: 90, gamma: 40 });
  level({ alpha: 40, beta: 90, gamma: 0 });
  for (const bad of [
    {}, { gamma: -40 },
    ...['beta', 'gamma'].flatMap(axis => [null, undefined, NaN, Infinity, -Infinity, '40']
      .map(value => ({ alpha: 0, beta: 0, gamma: 0, [axis]: value }))),
    { alpha: 0, beta: 181, gamma: 0 }, { alpha: 0, beta: -181, gamma: 0 },
    { alpha: 0, beta: 0, gamma: 91 }, { alpha: 0, beta: 0, gamma: -91 },
  ]) {
    assert.equal(screenTilt(bad), null);
    assert.deepEqual(createGestureTracker().sample(bad), { valid: false, sound: null, tilt: null });
  }
});

test('tilting toward or away from you never sounds', () => {
  for (const heading of [0, 135]) {
    const tracker = createGestureTracker();
    const readings = [...sweep(-170, 170, 10), ...sweep(170, -170, -10)].map(pitch => pose(0, { pitch, heading }));
    assert.deepEqual(play(tracker, readings), Array(readings.length).fill(null));
  }
});

test('nothing sounds before a whip, and a whip needs more than 30 degrees to the left', () => {
  const tracker = createGestureTracker();
  assert.deepEqual(play(tracker, [0, 45, 80, 140, 0, -SWING_DEGREES + 0.01].map(tilt => pose(tilt))),
    [null, null, null, null, null, null], 'the crack side and just under 30 degrees are silent');
  const result = tracker.sample(pose(-SWING_DEGREES - 0.01));
  assert.equal(result.sound, 'whip');
  assert.ok(Math.abs(result.tilt + SWING_DEGREES + 0.01) < 1e-9);
});

test('after a whip only a crack can follow, and only more than 30 degrees to the right', () => {
  const tracker = createGestureTracker();
  const tilts = [0, -40, -80, -40, -31, 0, 20, SWING_DEGREES - 0.01, SWING_DEGREES + 0.01, 60, 31, 0, -29, -31];
  assert.deepEqual(play(tracker, tilts.map(tilt => pose(tilt))),
    [null, 'whip', null, null, null, null, null, null, 'crack', null, null, null, null, 'whip']);
});

test('holding, shaking or creeping within one side never repeats a sound', () => {
  const tracker = createGestureTracker();
  const left = [-40, ...Array(20).fill(-90), -35, -100, -31, -140, -50].map(tilt => pose(tilt));
  assert.deepEqual(play(tracker, left).filter(Boolean), ['whip']);
  const right = [40, ...Array(20).fill(90), 35, 140, 31, 60].map(tilt => pose(tilt));
  assert.deepEqual(play(tracker, right).filter(Boolean), ['crack']);
});

test('real swings alternate in the right places at any heading or lean', () => {
  for (const heading of [0, 135]) {
    for (const pitch of [0, 30, 60]) {
      const tracker = createGestureTracker();
      const fired = [];
      for (let cycle = 0; cycle < 4; cycle += 1) {
        // Steps of 4 degrees avoid landing exactly on a threshold.
        for (const tilt of [...sweep(0, -112, -4), ...sweep(-108, 92, 4), ...sweep(88, 0, -4)]) {
          const result = tracker.sample(pose(tilt, { pitch, heading }));
          if (result.sound) fired.push([result.sound, tilt]);
        }
      }
      assert.deepEqual(fired, Array.from({ length: 4 }, () => [['whip', -32], ['crack', 32]]).flat(),
        `${heading} ${pitch}`);
    }
  }
});

test('the upright Euler singularity cannot jump between the sides', () => {
  const tracker = createGestureTracker();
  const upright = [{ alpha: 0, beta: 90, gamma: 40 }, { alpha: 40, beta: 90, gamma: 0 },
    { alpha: 359, beta: 90, gamma: 0 }, { alpha: 0, beta: 90, gamma: -1 }, { alpha: 0, beta: 89.9, gamma: 89.9 },
    { alpha: 180, beta: 90.1, gamma: -89.9 }];
  for (const event of upright) {
    const result = tracker.sample(event);
    assert.ok(Math.abs(result.tilt) < 0.2, JSON.stringify(event));
    assert.equal(result.sound, null);
  }
});

test('turning past upside down does not wrap from crack into whip', () => {
  const tracker = createGestureTracker();
  assert.deepEqual(play(tracker, [-40, 40].map(tilt => pose(tilt))), ['whip', 'crack']);
  const over = [100, 150, 160, 175, 180, -175, -160, -151, -149].map(tilt => pose(tilt));
  assert.deepEqual(play(tracker, over), [null, null, null, null, null, null, null, null, 'whip'],
    'within 30 degrees of upside down is neither side');
});

test('a phone lying nearly flat is ignored without losing its place', () => {
  const tracker = createGestureTracker();
  assert.equal(tracker.sample(pose(-40)).sound, 'whip');
  for (const pitch of [71, 80, 90, 100, 109]) {
    for (const tilt of [-120, -60, 60, 120]) {
      assert.deepEqual(tracker.sample(pose(tilt, { pitch })), { valid: true, sound: null, tilt: null });
    }
  }
  assert.equal(tracker.sample(pose(-60, { pitch: 69 })).sound, null, 'still waiting for the crack');
  assert.equal(tracker.sample(pose(40, { pitch: 30 })).sound, 'crack');
});

test('invalid readings neither reset nor advance the alternation', () => {
  const tracker = createGestureTracker();
  assert.equal(tracker.sample(pose(-40)).sound, 'whip');
  for (const bad of [{}, { alpha: 0, beta: null, gamma: 0 }, { alpha: 0, beta: 0, gamma: NaN }]) {
    assert.equal(tracker.sample(bad).valid, false);
  }
  assert.equal(tracker.sample(pose(-60)).sound, null);
  assert.equal(tracker.sample(pose(40)).sound, 'crack');
});

test('reset starts again with a whip', () => {
  const tracker = createGestureTracker();
  assert.equal(tracker.sample(pose(-40)).sound, 'whip');
  tracker.reset();
  assert.deepEqual(play(tracker, [40, -40, 40].map(tilt => pose(tilt))), [null, 'whip', 'crack']);
});
