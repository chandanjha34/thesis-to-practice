import { PortfolioLab } from "@/components/portfolio-lab";

export default function Home() {
  return (
    <main className="relative min-h-screen overflow-hidden">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-[70vh] hero-grid" />

      <header className="relative mx-auto flex w-full max-w-6xl items-center justify-between px-6 pb-2 pt-8">
        <div className="reveal-fade">
          <p className="font-display text-2xl tracking-tight text-ink md:text-3xl">
            Prospectfolio
          </p>
          <p className="mt-1 text-xs uppercase tracking-[0.2em] text-teal-900/55">
            Behavioural portfolio lab
          </p>
        </div>
        <a
          href="#lab"
          className="rounded-full border border-teal-950/15 bg-white/60 px-4 py-2 text-sm text-ink/80 backdrop-blur transition hover:bg-white"
        >
          Open the lab
        </a>
      </header>

      <section className="relative mx-auto grid w-full max-w-6xl gap-10 px-6 pb-16 pt-10 md:grid-cols-[1.15fr_0.85fr] md:pb-20 md:pt-16">
        <div className="reveal-up space-y-6">
          <h1 className="font-display text-4xl leading-[1.05] text-ink md:text-6xl">
            Build portfolios the way real investors feel risk.
          </h1>
          <p className="max-w-xl text-base leading-relaxed text-ink/70 md:text-lg">
            Turn Cumulative Prospect Theory, Data Envelopment Analysis, and MARCOS
            ranking into a hands-on stock selection tool — the practical slice of
            research on behavioural portfolio optimisation.
          </p>
          <div className="flex flex-wrap gap-3">
            <a
              href="#lab"
              className="inline-flex items-center rounded-full bg-teal-800 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-teal-900"
            >
              Explore rankings
            </a>
            <a
              href="#why"
              className="inline-flex items-center rounded-full border border-teal-950/15 bg-white/50 px-5 py-2.5 text-sm text-ink/80"
            >
              Why this project
            </a>
          </div>
        </div>

        <div className="float-soft relative hidden md:block">
          <div className="absolute -inset-4 rounded-[2rem] bg-gradient-to-br from-teal-700/20 via-transparent to-amber-600/20 blur-2xl" />
          <div className="relative overflow-hidden rounded-[1.6rem] border border-teal-950/10 bg-[#102823] p-6 text-[#e8f2ee] shadow-[0_30px_80px_-40px_rgba(8,40,34,0.8)]">
            <p className="font-mono text-[11px] uppercase tracking-[0.24em] text-teal-200/70">
              Thesis → product
            </p>
            <p className="mt-4 font-display text-2xl leading-snug">
              CPT scores assets. DEA judges efficiency. MARCOS breaks ties. You get
              a behavioural portfolio you can compare to Markowitz.
            </p>
            <div className="mt-8 grid grid-cols-3 gap-3 text-center">
              {[
                ["CPT", "Behaviour"],
                ["DEA", "Efficiency"],
                ["MCDA", "Ranking"],
              ].map(([k, v]) => (
                <div key={k} className="rounded-xl bg-white/5 px-2 py-3">
                  <p className="font-display text-lg text-teal-100">{k}</p>
                  <p className="text-[11px] uppercase tracking-wide text-teal-100/55">
                    {v}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section id="why" className="relative mx-auto w-full max-w-6xl px-6 pb-12">
        <div className="grid gap-8 md:grid-cols-3">
          {[
            {
              title: "From paper to product",
              body: "The thesis studies how loss aversion and probability weighting change portfolio choice versus classical mean–variance theory.",
            },
            {
              title: "One usable workflow",
              body: "Score → rank → select → compare. No research platform scaffolding — just the decision loop an analyst can run.",
            },
            {
              title: "Explainable knobs",
              body: "Change λ, α, β, γ and immediately see which Nifty-style names rise, and how behavioural portfolios trade off against MV.",
            },
          ].map((item) => (
            <div key={item.title} className="space-y-2 border-t border-teal-950/15 pt-4">
              <h2 className="font-display text-xl text-ink">{item.title}</h2>
              <p className="text-sm leading-relaxed text-ink/65">{item.body}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="lab" className="relative mx-auto w-full max-w-6xl px-6 pb-24">
        <PortfolioLab />
      </section>

      <footer className="border-t border-teal-950/10 bg-white/40 px-6 py-8 text-center text-sm text-ink/55">
        Educational demo inspired by research on Cumulative Prospect Theory in
        portfolio optimisation, multi-criteria decision analysis, and data
        envelopment analysis. Synthetic Nifty-style returns — not investment advice.
      </footer>
    </main>
  );
}
