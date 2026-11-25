# Part 1: Risk Control System

> Build the map first; details come later.

This part answers three questions:

1. What does Douyin's risk control actually check?
2. What is each of the seven signature headers responsible for?
3. Which local SDK components generate these headers?

## In this part

- [Chapter 1: Risk Control System Overview](./chapter_overview/README.md)
  - 1.1 Three-layer risk control model
  - 1.2 Seven signature headers and plaintext context
  - 1.3 Local SDK component mapping
  - 1.4 Version evolution: 39.4 → 41.2

## After reading, you should be able to

- explain the division of labor among the "device layer / network layer / behavior layer" in one sentence;
- distinguish a "plaintext declaration" from a "signature proof", and explain why inconsistency between the two is more common than a badly computed signature;
- map each signature header to its corresponding native library;
- state the two most important algorithm changes around 41.1.

> 💡 **Suggestion**: don't rush to memorize parameter names in this part; first draw the relationship among "three layers + two header groups + four libraries".
