# Part 3: Registration and Trust

> Registration is not "sending one request"; it is an ordered, timed, stateful chain.

This part breaks the process down in cold-start order:

1. Establish the clock baseline first;
2. Then walk the registration chain;
3. Construct the registration plaintext;
4. Obtain two kinds of token;
5. Complete the nurture chain and activation;
6. Warm up trust with TrustChain.

## What This Part Covers

- [Chapter 3: Device Registration Flow](./chapter_registration/README.md)
  - 3.1 Cold Start Sequence and Clock Baseline
  - 3.2 Registration Chain Breakdown
  - 3.3 Registration Plaintext Body Structure
  - 3.4 sec_device_token and SDI Token
  - 3.5 Nurture and Activation Chains
  - 3.6 TrustChain Warm-up

## After Reading, You Should Be Able To

- Write the constraint `boot_time ≤ first_launch ≤ app_start ≤ request time`, and explain why an inversion is anomalous;
- State the order of the six-step registration chain, and explain why "out of order" does not necessarily fail but does lead to lower weight;
- Distinguish the lifecycles of `sec_device_token` and SDI token;
- Explain why "finishing registration plus nurture within 1 second" is itself an anomalous signature.

> 💡 **Key Perspective**: The server looks not only at "what you sent", but also at "when and in what order you sent it".
