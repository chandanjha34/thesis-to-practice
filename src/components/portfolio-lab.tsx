"use client";

import { useMemo, useState, useTransition } from "react";
import {
  Area,
  CartesianGrid,
  ComposedChart,
  Legend,
  ResponsiveContainer,
  Scatter,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { ArrowRight, Brain, LineChart, Scale, Sparkles } from "lucide-react";
import {
  analyzeUniverse,
  DEFAULT_CPT_PARAMS,
  SAMPLE_ASSETS,
  type AnalysisResult,
  type CptParams,
} from "@/lib/portfolio";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { cn } from "@/lib/utils";

function pct(x: number, digits = 1): string {
  return `${(x * 100).toFixed(digits)}%`;
}

function num(x: number, digits = 3): string {
  return x.toFixed(digits);
}

const PRESETS: { label: string; params: Partial<CptParams> }[] = [
  { label: "Classic TK", params: { alpha: 0.88, beta: 0.88, lambda: 2.25, gamma: 0.61, delta: 0.69 } },
  { label: "Loss-averse", params: { lambda: 3.2, alpha: 0.85, beta: 0.9 } },
  { label: "Near-rational", params: { lambda: 1.2, alpha: 0.95, beta: 0.95, gamma: 0.9, delta: 0.9 } },
];

export function PortfolioLab() {
  const [params, setParams] = useState<CptParams>({ ...DEFAULT_CPT_PARAMS });
  const [topK, setTopK] = useState(10);
  const [isPending, startTransition] = useTransition();
  const [result, setResult] = useState<AnalysisResult>(() =>
    analyzeUniverse(SAMPLE_ASSETS, DEFAULT_CPT_PARAMS, 10),
  );

  const run = (next: CptParams, k = topK) => {
    startTransition(() => {
      setResult(analyzeUniverse(SAMPLE_ASSETS, next, k));
    });
  };

  const update = (patch: Partial<CptParams>) => {
    const next = { ...params, ...patch };
    setParams(next);
    run(next);
  };

  const chartData = useMemo(() => {
    const mv = result.frontierMv
      .filter((p) => p.kind === "mean-variance")
      .map((p) => ({ risk: p.risk, mv: p.return, label: p.label }));
    const assets = result.frontierMv
      .filter((p) => p.kind === "asset")
      .map((p) => ({ risk: p.risk, asset: p.return, label: p.label }));
    const cpt = result.frontierCpt.map((p) => ({
      risk: p.risk,
      cpt: p.return,
      label: p.label,
    }));
    return { mv, assets, cpt };
  }, [result]);

  const ranked = useMemo(
    () => [...result.assets].sort((a, b) => a.cptRank - b.cptRank),
    [result.assets],
  );

  return (
    <div className="space-y-10">
      <section className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="space-y-5">
          <p className="font-mono text-xs uppercase tracking-[0.22em] text-teal-800/70">
            Interactive lab · CPT × DEA × MARCOS
          </p>
          <h2 className="font-display text-3xl leading-tight text-ink md:text-4xl">
            Tune behavioural risk attitudes and watch rankings and portfolios re-form.
          </h2>
          <p className="max-w-xl text-base leading-relaxed text-ink/70">
            This sandbox follows the thesis pipeline: score assets with Cumulative
            Prospect Theory, rank them with DEA cross-efficiency, break ties with
            MARCOS, then compare behavioural portfolios against a classical
            mean–variance benchmark on a Nifty-style universe.
          </p>
          <div className="flex flex-wrap gap-2">
            {PRESETS.map((preset) => (
              <Button
                key={preset.label}
                variant="outline"
                size="sm"
                className="border-teal-900/15 bg-white/60"
                onClick={() => update(preset.params)}
              >
                {preset.label}
              </Button>
            ))}
          </div>
        </div>

        <div className="rounded-2xl border border-teal-950/10 bg-white/70 p-5 shadow-[0_20px_60px_-40px_rgba(12,60,50,0.45)] backdrop-blur">
          <div className="mb-4 flex items-center justify-between">
            <h3 className="font-display text-lg text-ink">Behavioural knobs</h3>
            <Badge variant="secondary" className={cn(isPending && "animate-pulse")}>
              {isPending ? "Recomputing…" : "Live"}
            </Badge>
          </div>
          <ParamSlider
            label="Loss aversion λ"
            hint="How painfully losses weigh vs gains"
            value={params.lambda}
            min={1}
            max={4}
            step={0.05}
            onChange={(lambda) => update({ lambda })}
          />
          <ParamSlider
            label="Gain curvature α"
            hint="Diminishing sensitivity for gains"
            value={params.alpha}
            min={0.5}
            max={1}
            step={0.01}
            onChange={(alpha) => update({ alpha })}
          />
          <ParamSlider
            label="Loss curvature β"
            hint="Diminishing sensitivity for losses"
            value={params.beta}
            min={0.5}
            max={1}
            step={0.01}
            onChange={(beta) => update({ beta })}
          />
          <ParamSlider
            label="Probability weight γ (gains)"
            hint="Overweighting of small probabilities"
            value={params.gamma}
            min={0.4}
            max={1}
            step={0.01}
            onChange={(gamma) => update({ gamma })}
          />
          <div className="mt-4">
            <div className="mb-2 flex items-center justify-between text-sm">
              <span className="text-ink/80">Top / bottom CPT group size</span>
              <span className="font-mono text-ink">{topK}</span>
            </div>
            <Slider
              value={[topK]}
              min={5}
              max={15}
              step={1}
              onValueChange={([k]) => {
                setTopK(k);
                run(params, k);
              }}
            />
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricTile
          icon={<Brain className="h-4 w-4" />}
          title="Top-CPT portfolio"
          returnPct={result.portfolios.topCpt.expectedReturn}
          vol={result.portfolios.topCpt.volatility}
          sharpe={result.portfolios.topCpt.sharpe}
          cpt={result.portfolios.topCpt.cptValue}
          accent="teal"
        />
        <MetricTile
          icon={<Scale className="h-4 w-4" />}
          title="Mean–variance"
          returnPct={result.portfolios.meanVariance.expectedReturn}
          vol={result.portfolios.meanVariance.volatility}
          sharpe={result.portfolios.meanVariance.sharpe}
          cpt={result.portfolios.meanVariance.cptValue}
          accent="amber"
        />
        <MetricTile
          icon={<LineChart className="h-4 w-4" />}
          title="DEA × CPT"
          returnPct={result.portfolios.deaCross.expectedReturn}
          vol={result.portfolios.deaCross.volatility}
          sharpe={result.portfolios.deaCross.sharpe}
          cpt={result.portfolios.deaCross.cptValue}
          accent="sky"
        />
        <MetricTile
          icon={<Sparkles className="h-4 w-4" />}
          title="Bottom-CPT (control)"
          returnPct={result.portfolios.bottomCpt.expectedReturn}
          vol={result.portfolios.bottomCpt.volatility}
          sharpe={result.portfolios.bottomCpt.sharpe}
          cpt={result.portfolios.bottomCpt.cptValue}
          accent="rose"
        />
      </section>

      <Tabs defaultValue="frontier" className="space-y-4">
        <TabsList className="bg-white/70">
          <TabsTrigger value="frontier">Efficient frontier</TabsTrigger>
          <TabsTrigger value="ranks">Asset ranks</TabsTrigger>
          <TabsTrigger value="weights">Portfolio weights</TabsTrigger>
          <TabsTrigger value="pipeline">Method pipeline</TabsTrigger>
        </TabsList>

        <TabsContent value="frontier">
          <Card className="border-teal-950/10 bg-white/75">
            <CardHeader>
              <CardTitle className="font-display text-xl">
                Risk–return map: behavioural vs classical
              </CardTitle>
            </CardHeader>
            <CardContent className="h-[380px]">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart margin={{ top: 10, right: 10, left: 0, bottom: 10 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#0f3d3422" />
                  <XAxis
                    type="number"
                    dataKey="risk"
                    name="Risk"
                    unit="%"
                    tick={{ fill: "#1c2b27", fontSize: 12 }}
                    label={{ value: "Annualised volatility (%)", position: "insideBottom", offset: -2 }}
                  />
                  <YAxis
                    type="number"
                    name="Return"
                    unit="%"
                    tick={{ fill: "#1c2b27", fontSize: 12 }}
                    label={{ value: "Expected return (%)", angle: -90, position: "insideLeft" }}
                  />
                  <Tooltip
                    formatter={(value) =>
                      typeof value === "number" ? `${value.toFixed(2)}%` : value
                    }
                  />
                  <Legend />
                  <Area
                    data={chartData.mv}
                    dataKey="mv"
                    name="Mean–variance frontier"
                    stroke="#c45c26"
                    fill="#c45c2622"
                    type="monotone"
                  />
                  <Scatter
                    data={chartData.cpt}
                    dataKey="cpt"
                    name="CPT portfolios"
                    fill="#0f766e"
                  />
                  <Scatter
                    data={chartData.assets}
                    dataKey="asset"
                    name="Individual assets"
                    fill="#64748b"
                    fillOpacity={0.55}
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="ranks">
          <Card className="border-teal-950/10 bg-white/75 overflow-hidden">
            <CardHeader>
              <CardTitle className="font-display text-xl">
                CPT, DEA cross-efficiency, and MARCOS ranks
              </CardTitle>
            </CardHeader>
            <CardContent className="overflow-x-auto">
              <table className="w-full min-w-[720px] text-left text-sm">
                <thead className="border-b border-teal-950/10 text-xs uppercase tracking-wide text-ink/55">
                  <tr>
                    <th className="py-2 pr-3">Ticker</th>
                    <th className="py-2 pr-3">Sector</th>
                    <th className="py-2 pr-3">Return</th>
                    <th className="py-2 pr-3">Vol</th>
                    <th className="py-2 pr-3">CPT</th>
                    <th className="py-2 pr-3">CPT #</th>
                    <th className="py-2 pr-3">Cross-eff</th>
                    <th className="py-2 pr-3">DEA #</th>
                    <th className="py-2 pr-3">MARCOS #</th>
                  </tr>
                </thead>
                <tbody>
                  {ranked.map((a) => (
                    <tr key={a.ticker} className="border-b border-teal-950/5 hover:bg-teal-50/50">
                      <td className="py-2.5 pr-3 font-medium text-ink">{a.ticker}</td>
                      <td className="py-2.5 pr-3 text-ink/65">{a.sector}</td>
                      <td className="py-2.5 pr-3 font-mono">{pct(a.meanReturn)}</td>
                      <td className="py-2.5 pr-3 font-mono">{pct(a.volatility)}</td>
                      <td className="py-2.5 pr-3 font-mono">{num(a.cptValue)}</td>
                      <td className="py-2.5 pr-3 font-mono">{a.cptRank}</td>
                      <td className="py-2.5 pr-3 font-mono">{num(a.crossEfficiency)}</td>
                      <td className="py-2.5 pr-3 font-mono">{a.deaRank}</td>
                      <td className="py-2.5 pr-3 font-mono">{a.marcosRank}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="weights">
          <div className="grid gap-4 lg:grid-cols-2">
            <WeightCard portfolio={result.portfolios.topCpt} />
            <WeightCard portfolio={result.portfolios.deaCross} />
            <WeightCard portfolio={result.portfolios.meanVariance} />
            <WeightCard portfolio={result.portfolios.bottomCpt} />
          </div>
        </TabsContent>

        <TabsContent value="pipeline">
          <Card className="border-teal-950/10 bg-white/75">
            <CardContent className="grid gap-6 p-6 md:grid-cols-4">
              {[
                {
                  step: "01",
                  title: "CPT scoring",
                  body: "Each stock’s return path is valued with a prospect value function and probability weighting — capturing loss aversion and probability distortion.",
                },
                {
                  step: "02",
                  title: "DEA efficiency",
                  body: "Variance is the input; CPT value and long-term return are outputs. Cross-efficiency averages peer evaluations for a tougher ranking.",
                },
                {
                  step: "03",
                  title: "MARCOS ranking",
                  body: "When many units sit on the DEA frontier, MARCOS benchmarks against ideal and anti-ideal solutions to produce a finer order.",
                },
                {
                  step: "04",
                  title: "Portfolio build",
                  body: "Top CPT / DEA names are mixed to maximise behavioural value, then compared with a classical mean–variance max-Sharpe portfolio.",
                },
              ].map((item) => (
                <div key={item.step} className="relative space-y-2">
                  <p className="font-mono text-xs text-teal-800/70">{item.step}</p>
                  <h4 className="font-display text-lg text-ink">{item.title}</h4>
                  <p className="text-sm leading-relaxed text-ink/65">{item.body}</p>
                </div>
              ))}
            </CardContent>
          </Card>
          <p className="mt-4 flex items-center gap-2 text-sm text-ink/60">
            <ArrowRight className="h-4 w-4" />
            Thesis core: Cumulative Prospect Theory in portfolio optimisation, MCDA, and DEA.
          </p>
        </TabsContent>
      </Tabs>
    </div>
  );
}

function ParamSlider({
  label,
  hint,
  value,
  min,
  max,
  step,
  onChange,
}: {
  label: string;
  hint: string;
  value: number;
  min: number;
  max: number;
  step: number;
  onChange: (v: number) => void;
}) {
  return (
    <div className="mb-4">
      <div className="mb-1 flex items-center justify-between gap-3">
        <div>
          <p className="text-sm text-ink/85">{label}</p>
          <p className="text-xs text-ink/50">{hint}</p>
        </div>
        <span className="font-mono text-sm text-ink">{value.toFixed(2)}</span>
      </div>
      <Slider
        value={[value]}
        min={min}
        max={max}
        step={step}
        onValueChange={([v]) => onChange(v)}
      />
    </div>
  );
}

function MetricTile({
  icon,
  title,
  returnPct,
  vol,
  sharpe,
  cpt,
  accent,
}: {
  icon: React.ReactNode;
  title: string;
  returnPct: number;
  vol: number;
  sharpe: number;
  cpt: number;
  accent: "teal" | "amber" | "sky" | "rose";
}) {
  const accents = {
    teal: "from-teal-700/15 to-transparent border-teal-800/15",
    amber: "from-amber-700/15 to-transparent border-amber-800/15",
    sky: "from-sky-700/15 to-transparent border-sky-800/15",
    rose: "from-rose-700/15 to-transparent border-rose-800/15",
  };
  return (
    <div
      className={cn(
        "rounded-2xl border bg-gradient-to-br p-4",
        accents[accent],
        "bg-white/70",
      )}
    >
      <div className="mb-3 flex items-center gap-2 text-ink/70">
        {icon}
        <p className="text-sm font-medium text-ink">{title}</p>
      </div>
      <p className="font-display text-3xl text-ink">{pct(returnPct)}</p>
      <p className="mt-1 text-xs text-ink/55">expected annual return</p>
      <dl className="mt-3 grid grid-cols-3 gap-2 text-xs">
        <div>
          <dt className="text-ink/45">Vol</dt>
          <dd className="font-mono text-ink">{pct(vol)}</dd>
        </div>
        <div>
          <dt className="text-ink/45">Sharpe</dt>
          <dd className="font-mono text-ink">{num(sharpe, 2)}</dd>
        </div>
        <div>
          <dt className="text-ink/45">CPT</dt>
          <dd className="font-mono text-ink">{num(cpt)}</dd>
        </div>
      </dl>
    </div>
  );
}

function WeightCard({
  portfolio,
}: {
  portfolio: AnalysisResult["portfolios"]["topCpt"];
}) {
  const pairs = portfolio.tickers
    .map((t, i) => ({ t, w: portfolio.weights[i] }))
    .sort((a, b) => b.w - a.w)
    .slice(0, 12);

  return (
    <Card className="border-teal-950/10 bg-white/75">
      <CardHeader>
        <CardTitle className="font-display text-lg">{portfolio.method}</CardTitle>
        <p className="text-sm text-ink/55">
          Return {pct(portfolio.expectedReturn)} · Vol {pct(portfolio.volatility)} ·
          CPT {num(portfolio.cptValue)}
        </p>
      </CardHeader>
      <CardContent className="space-y-2">
        {pairs.map(({ t, w }) => (
          <div key={t} className="grid grid-cols-[72px_1fr_48px] items-center gap-2 text-sm">
            <span className="font-medium text-ink">{t}</span>
            <div className="h-2 overflow-hidden rounded-full bg-teal-950/5">
              <div
                className="h-full rounded-full bg-teal-700/80 transition-all duration-500"
                style={{ width: `${Math.min(100, w * 100)}%` }}
              />
            </div>
            <span className="text-right font-mono text-ink/70">{pct(w, 1)}</span>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
