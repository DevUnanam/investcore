(function () {
  const { createElement: h } = React;

  const marketItems = [
    ["EUR/USD", "1.0834", "+0.18%"],
    ["GBP/USD", "1.2710", "+0.11%"],
    ["USD/JPY", "148.22", "-0.07%"],
    ["XAU/USD", "2,416.80", "+0.42%"],
    ["AAPL", "226.31", "+1.24%"],
    ["TSLA", "243.87", "-0.58%"],
    ["NVDA", "121.36", "+2.06%"],
    ["MSFT", "419.09", "+0.33%"],
  ];

  const slides = [
    ["Smart Bundles", "Starter, Growth, and Premium bundles with clear duration, range, and expected returns."],
    ["AI Signals", "Portfolio guidance and market context designed for confident decision making."],
    ["Fast Wallets", "Deposit, withdraw, and track transaction history from one clean dashboard."],
  ];

  const bundles = [
    ["Starter Bundle", "$1,000 - $5,000", "2 months", "8%", "Launch"],
    ["Growth Bundle", "$2,000 - $10,000", "3 months", "11%", "Popular"],
    ["Premium Bundle", "$3,000 - $15,000", "6 months", "15%", "Long term"],
  ];

  function Icon({ type }) {
    const paths = {
      chart: "M4 17l5-5 4 4 7-9M16 7h4v4",
      shield: "M12 3l7 3v5c0 5-3.4 8.2-7 10-3.6-1.8-7-5-7-10V6l7-3zM9 12l2 2 4-5",
      wallet: "M4 7h14a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V7zm13 5h3",
      cube: "M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3zm0 9l8-4.5M12 12v9M12 12L4 7.5",
      users: "M16 21v-2a4 4 0 00-4-4H6a4 4 0 00-4 4v2M9 11a4 4 0 100-8 4 4 0 000 8M22 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75",
    };
    return h("svg", { viewBox: "0 0 24 24", "aria-hidden": "true" }, h("path", { d: paths[type], fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }));
  }

  function MarketMarquee() {
    const row = marketItems.concat(marketItems);
    return h("div", { className: "market-marquee", "aria-label": "Market price ticker" },
      h("div", { className: "ticker-track" }, row.map((item, index) =>
        h("span", { className: "ticker-item", key: `${item[0]}-${index}` },
          h("strong", null, item[0]), h("b", null, item[1]), h("em", { className: item[2][0] === "+" ? "up" : "down" }, item[2])
        )
      ))
    );
  }

  function App() {
    const [activeSlide, setActiveSlide] = React.useState(0);
    React.useEffect(() => {
      const timer = setInterval(() => setActiveSlide((value) => (value + 1) % slides.length), 4200);
      return () => clearInterval(timer);
    }, []);

    return h("main", null,
      h("section", { className: "hero" },
        h("nav", { className: "nav" },
          h("a", { className: "brand", href: "#" }, "Nervex ", h("span", null, "AI")),
          h("div", { className: "nav-links" },
            h("a", { href: "#bundles" }, "Bundles"),
            h("a", { href: "#insights" }, "Insights"),
            h("a", { href: "#security" }, "Security")
          ),
          h("a", { className: "nav-cta", href: "#start" }, "Get Started")
        ),
        h("div", { className: "hero-grid" },
          h("div", { className: "hero-copy" },
            h("h1", null, "Invest smarter with confidence"),
            h("p", null, "AI-powered insights, guided investment bundles, and a secure wallet experience built to help everyday investors grow with clarity."),
            h("div", { className: "hero-actions" },
              h("a", { className: "button primary", href: "#start" }, "Create Account"),
              h("a", { className: "button secondary", href: "#bundles" }, "Explore Bundles")
            )
          ),
          h("div", { className: "phone-preview", "aria-label": "Nervex AI app preview" },
            h("div", { className: "phone-top" }, h("strong", null, "Nervex ", h("span", null, "AI")), h("i", null, "3")),
            h("div", { className: "balance-card" }, h("small", null, "Total Portfolio Balance"), h("b", null, "$24,750.60"), h("div", null, h("span", null, "Invested $20,500"), h("em", null, "+20.73%"))),
            h("div", { className: "mini-grid" }, ["7 Active Bundles", "$28,980 Value", "18 Days"].map((text, i) => h("div", { key: text }, h(Icon, { type: ["cube", "chart", "shield"][i] }), h("strong", null, text)))),
            h("div", { className: "phone-actions" }, h("button", null, "Add Money"), h("button", null, "Withdraw"))
          )
        )
      ),
      h(MarketMarquee),
      h("section", { className: "section split", id: "insights" },
        h("div", null, h("h2", null, "A portfolio home that feels calm, clear, and alive."), h("p", null, "Track balances, investment performance, returns, deposits, withdrawals, and referral rewards in a simple interface inspired by modern mobile banking.")),
        h("div", { className: "carousel" },
          h("div", { className: "slide-card" }, h(Icon, { type: activeSlide === 1 ? "chart" : activeSlide === 2 ? "wallet" : "shield" }), h("h3", null, slides[activeSlide][0]), h("p", null, slides[activeSlide][1])),
          h("div", { className: "dots" }, slides.map((_, index) => h("button", { key: index, onClick: () => setActiveSlide(index), className: index === activeSlide ? "active" : "", "aria-label": `Show slide ${index + 1}` })))
        )
      ),
      h("section", { className: "section", id: "bundles" },
        h("div", { className: "section-heading" }, h("h2", null, "Investment bundles for every stage"), h("p", null, "Clear ranges, clear timelines, and projected returns users can compare at a glance.")),
        h("div", { className: "bundle-grid" }, bundles.map((bundle) =>
          h("article", { className: "bundle-card", key: bundle[0] },
            h("span", null, bundle[4]), h(Icon, { type: bundle[0] === "Starter Bundle" ? "wallet" : bundle[0] === "Growth Bundle" ? "chart" : "shield" }),
            h("h3", null, bundle[0]),
            h("dl", null, h("dt", null, "Range"), h("dd", null, bundle[1]), h("dt", null, "Duration"), h("dd", null, bundle[2]), h("dt", null, "Projected Return"), h("dd", null, bundle[3])),
            h("a", { href: "#start" }, "View Details")
          )
        ))
      ),
      h("section", { className: "section security", id: "security" },
        h("div", { className: "trust-icon" }, h(Icon, { type: "shield" })),
        h("div", null, h("h2", null, "Secure by design, ready for real product growth."), h("p", null, "This first stage keeps the landing page responsive and Render-ready while leaving room for Django auth, React dashboards, payment flows, agents, and bundle management in later stages."))
      ),
      h("section", { className: "start", id: "start" },
        h("h2", null, "Start building wealth with Nervex AI"),
        h("p", null, "Join the waitlist for early access to smarter portfolio tools."),
        h("form", null, h("input", { type: "email", placeholder: "Enter your email", "aria-label": "Email address" }), h("button", { type: "submit" }, "Join Waitlist"))
      )
    );
  }

  ReactDOM.createRoot(document.getElementById("nervex-landing")).render(h(App));
}());
