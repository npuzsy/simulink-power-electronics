# Table 7 State Vector Sequences

This is the source-of-truth state sequence standard from the guide PDF, normalized for implementation.

## Token Mapping

- `n -> 0`
- `o -> 1`
- `p -> 2`

Each token triplet maps to `[Sa Sb Sc]`.

## Large Sector I

- `I1`: `onn oon ooo poo ooo oon onn`
- `I2`: `oon ooo poo ppo poo ooo oon`
- `I3`: `onn oon pon poo pon oon onn`
- `I4`: `oon pon poo ppo poo pon oon`
- `I5`: `onn pnn pon poo pon pnn onn`
- `I6`: `oon pon ppn ppo ppn pon oon`

## Large Sector II

- `II1`: `oon ooo opo ppo opo ooo oon`
- `II2`: `non oon ooo opo ooo oon non`
- `II3`: `oon opn opo ppo opo opn oon`
- `II4`: `non oon opn opo opn oon non`
- `II5`: `oon opn ppn ppo ppn opn oon`
- `II6`: `non npn opn opo opn npn non`

## Large Sector III

- `III1`: `non noo ooo opo ooo noo non`
- `III2`: `noo ooo opo opp opo ooo noo`
- `III3`: `non noo npo opo npo noo non`
- `III4`: `noo npo opo opp opo npo noo`
- `III5`: `non npn npo opo npo npn non`
- `III6`: `noo npo npp opp npp npo noo`

## Large Sector IV

- `IV1`: `noo ooo oop opp oop ooo noo`
- `IV2`: `nno noo ooo oop ooo noo nno`
- `IV3`: `noo nop oop opp oop nop noo`
- `IV4`: `nno noo nop oop nop noo nno`
- `IV5`: `noo nop npp opp npp nop noo`
- `IV6`: `nno nnp nop oop nop nnp nno`

## Large Sector V

- `V1`: `nno ono ooo oop ooo ono nno`
- `V2`: `ono ooo oop pop oop ooo ono`
- `V3`: `nno ono onp oop onp ono nno`
- `V4`: `ono onp oop pop oop onp ono`
- `V5`: `nno nnp onp oop onp nnp nno`
- `V6`: `ono onp pnp pop pnp onp ono`

## Large Sector VI

- `VI1`: `ono ooo poo pop poo ooo ono`
- `VI2`: `onn ono ooo poo ooo ono onn`
- `VI3`: `ono pno poo pop poo pno ono`
- `VI4`: `onn ono pno poo pno ono onn`
- `VI5`: `ono pno pnp pop pnp pno ono`
- `VI6`: `onn pnn pno poo pno pnn onn`

## Four-Constant Implementation Pattern

Many Simulink implementations store only four constants per small sector because the seven-segment sequence is symmetric:

`v1 v2 v3 v4 v3 v2 v1`

When checking model constants, compare the stored constants against the first four vectors in the sequence above.
