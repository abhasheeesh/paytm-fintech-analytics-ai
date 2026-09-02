
# Blockchain and Crypto Risk Appendix

## 1. Stablecoin and DeFi/DAO Risk

A hypothetical Paytm Crypto Insights feature would need to distinguish clearly between different types of stablecoins rather than treating the label "stablecoin" as evidence that an asset is inherently low-risk. A fiat-collateralized stablecoin attempts to maintain its peg through reserves such as cash or short-duration financial assets. Its main risks therefore include the quality and transparency of those reserves, the reliability of the custodian, redemption liquidity, and the possibility that the issuer does not actually hold sufficient assets to meet redemptions. An algorithmic stablecoin is structurally different because its peg depends primarily on market incentives, token-supply adjustments, or relationships with another crypto token instead of fully backed fiat reserves. This creates a much greater possibility of a feedback loop in which declining confidence causes both the supporting mechanism and the stablecoin itself to fall simultaneously.

For a retail-facing watchlist, Paytm should therefore display stablecoin type, reserve structure, audit or attestation information, liquidity, and any history of losing its peg. A simple "stable" classification would otherwise give users a misleading impression of safety.

DeFi and DAO products create a second governance problem. Tokenomics can concentrate voting power among founders, early investors, large token holders, or entities able to accumulate governance tokens cheaply. A project can describe itself as decentralized while effective decision-making remains concentrated among a small number of participants. Governance proposals can also alter fees, collateral requirements, treasury usage, or protocol rules after an investor has entered the ecosystem. A Paytm watchlist should therefore surface governance concentration, token-distribution risk, smart-contract risk, and the extent to which users depend on decisions made by token holders or protocol developers.

## 2. Crypto as an Asset Class

I would recommend a maximum crypto allocation of 5% for a retail advisory product, with a lower or zero allocation being appropriate for conservative investors. The argument for some exposure is primarily diversification: crypto returns can show relatively low correlation with traditional asset classes, so a small position may change overall portfolio behaviour. At the same time, correlation alone is not sufficient to justify a large allocation.

Unlike a bond or an equity claim on a cash-generating business, many cryptocurrencies provide no conventional stream of dividends, interest, or underlying operating cash flows from which intrinsic value can be estimated. This limits the usefulness of traditional CAPM-style and fundamental valuation frameworks. Historical crypto returns are also characterized by extreme volatility, heavy tails and, in some periods, positive skewness. Large positive outcomes can make historical average returns appear attractive while masking the probability of severe losses.

Reported historical performance also suffers from survivorship bias because failed tokens disappear while successful assets remain visible in datasets and investor discussions. Transaction costs, spreads, custody costs and market-impact costs can further reduce the diversification benefit that appears in frictionless portfolio calculations.

For these reasons, I would not treat crypto as a core strategic allocation for Paytm Money customers. A 5% ceiling allows an investor who explicitly understands and accepts the risk to obtain limited exposure without allowing a highly volatile asset to dominate total portfolio outcomes. The allocation should also be accompanied by suitability checks and explicit warnings that historical upside does not imply a dependable expected return.

## 3. T.A.N.G. Fraud Framework

Two T.A.N.G. vectors appear particularly relevant to a platform combining UPI or wallet payments, lending and wealth products.

The first is **Authority**. A fraudster may impersonate Paytm, a bank employee, a regulator, or a customer-support representative and claim that a user's account, KYC status, loan, or investment requires immediate action. The attacker may then request an OTP, persuade the user to approve a UPI collect request, or direct the user to a malicious link. A useful bank-side real-time defence would combine device and behavioural risk scoring with transaction friction. A high-value transaction initiated from a new device or immediately after suspicious account changes could trigger step-up authentication, a prominent scam warning, or temporary manual review.

The second is **Greed/Temptation**, particularly in wealth and crypto-related contexts. Fraudsters can advertise guaranteed investment returns, fake token opportunities, instant loan benefits, or limited-time rewards and then direct victims toward fraudulent payment addresses or accounts. The real-time defence should include beneficiary-risk scoring and network-level monitoring for accounts receiving suspicious numbers of payments from unrelated customers. Transfers to newly created or previously flagged beneficiaries could trigger additional confirmation explaining the specific scam pattern before money leaves the user's account.

T.A.N.G. is useful because these attacks are not purely technical failures. They exploit the psychological reason a user acts. Effective fraud controls therefore need to combine transaction analytics with interventions designed around the social-engineering pressure present at the moment of payment.
