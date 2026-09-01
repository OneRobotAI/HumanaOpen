# Electronics & Wiring

Power, control board and camera wiring notes for HumanaOpen.

> Placeholder — fill in your actual wiring diagram, pinout and power notes.

## Power

- Supply voltage: **12V** (arms/servos).
- Current budget: ...

## Control board (Host)

- Board: ...
- Serial ports used: `port1` (left arm + head), `port2` (right arm), `port3` (base wheels).
- Follower connecting cables: ...

## Cameras

- `head` → `/dev/video0`
- `left_wrist` → `/dev/video2`
- `right_wrist` → `/dev/video4`
- `chest` → `/dev/video6` (optional)

See the README **Camera devices & fps** section for the tested devices.

## Wiring diagram

_(add your diagram image here)_

## Grounding / safety

- Common ground between board and servo bus.
- Fuse / polarity protection.
