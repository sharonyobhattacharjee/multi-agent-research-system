
"use client";

import { useState } from "react";
import {
  Activity,
  ArrowUpRight,
  BrainCircuit,
  CheckCircle2,
  Clock3,
  Command,
  FileSearch,
  FileText,
  Globe2,
  History,
  Layers3,
  Menu,
  Network,
  Search,
  Send,
  Settings2,
  ShieldCheck,
  Sparkles,
  Zap,
  LoaderCircle,
} from "lucide-react";

const agents = [
  {
    number: "01",
    name: "SEARCH ENGINE",
    description: "Web discovery and source identification",
    icon: Search,
    color: "text-cyan-400",
    background: "bg-cyan-400/10",
  },
  {
    number: "02",
    name: "INTELLIGENCE READER",
    description: "Webpage extraction and content analysis",
    icon: FileSearch,
    color: "text-blue-400",
    background: "bg-blue-400/10",
  },
  {
    number: "03",
    name: "REPORT SYNTHESIS",
    description: "Research synthesis and report generation",
    icon: BrainCircuit,
    color: "text-violet-400",
    background: "bg-violet-400/10",
  },
  {
    number: "04",
    name: "QUALITY CRITIC",
    description: "Evaluation, verification and feedback",
    icon: ShieldCheck,
    color: "text-emerald-400",
    background: "bg-emerald-400/10",
  },
];

const suggestions = [
  "The future of autonomous AI agents",
  "Impact of generative AI on software engineering",
  "Latest advances in quantum computing",
  "Solid-state battery technology in 2026",
];

const tabs = [
  { name: "Research Report", icon: FileText },
  { name: "Critic Review", icon: ShieldCheck },
  { name: "Sources", icon: Globe2 },
  { name: "Raw Intelligence", icon: Layers3 },
];

export default function Home() {
  const [topic, setTopic] = useState("");
  const [activeTab, setActiveTab] = useState("Research Report");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [researchData, setResearchData] = useState<any>(null);
  const [isResearching, setIsResearching] = useState(false);
  const [notice, setNotice] = useState("");

  // Extract source URLs from the research data.
  const sourceText = [
    researchData?.search_results || "",
    researchData?.scraped_content || "",
  ].join("\n");

  const sourceUrls = [
    ...new Set(
      (sourceText.match(/https?:\/\/[^\s"'\\\])>,]+/g) || []).map(
        (url: string) => url.replace(/[.,;]+$/, "")
      )
    ),
  ];

  // RESEARCH FUNCTION
  async function handleResearch() {
    if (!topic.trim()) {
      setNotice("Enter a research topic to continue.");
      return;
    }

    setIsResearching(true);
    setResearchData(null);
    setNotice("Connecting to NEXUS research engine...");

    try {
      const response = await fetch("http://127.0.0.1:8000/api/research", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          topic: topic.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Research failed.");
      }

      setResearchData(data);
      setActiveTab("Research Report");
      setNotice("Research completed successfully.");
    } catch (error) {
      console.error("NEXUS API Error:", error);

      setNotice(
        error instanceof Error
          ? error.message
          : "Could not connect to backend."
      );
    } finally {
      setIsResearching(false);
    }
  }

  // ICON FOR ACTIVE TAB
  function ActiveTabIcon() {
    if (activeTab === "Research Report") {
      return <FileText className="text-cyan-400" size={23} />;
    }

    if (activeTab === "Critic Review") {
      return <ShieldCheck className="text-cyan-400" size={23} />;
    }

    if (activeTab === "Sources") {
      return <Globe2 className="text-cyan-400" size={23} />;
    }

    return <Layers3 className="text-cyan-400" size={23} />;
  }

  // RESEARCH OUTPUT
  function renderResearchOutput() {
    if (isResearching) {
      return (
        <div className="flex min-h-[230px] flex-col items-center justify-center px-5 py-10 text-center">
          <LoaderCircle className="mb-4 h-9 w-9 animate-spin text-cyan-400" />

          <h4 className="text-sm font-semibold text-slate-200">
            NEXUS is working on your research
          </h4>

          <p className="mt-2 max-w-sm text-xs leading-6 text-slate-500">
            Your AI agents are processing the topic. This may take a little
            while.
          </p>
        </div>
      );
    }

    if (!researchData) {
      return (
        <div className="flex min-h-[230px] flex-col items-center justify-center px-5 py-10 text-center">
          <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl border border-cyan-400/15 bg-cyan-400/[0.06]">
            <ActiveTabIcon />
          </div>

          <h4 className="text-sm font-semibold text-slate-300">
            {activeTab} will appear here
          </h4>

          <p className="mt-2 max-w-sm text-xs leading-6 text-slate-600">
            Start a research session to populate this workspace with findings
            from your AI agents.
          </p>
        </div>
      );
    }

    if (activeTab === "Research Report") {
      return (
        <div className="p-5 md:p-8">
          <div className="mb-5 flex items-center gap-2">
            <FileText size={16} className="text-cyan-400" />
            <h4 className="text-sm font-semibold text-white">
              Research Report
            </h4>
          </div>

          <pre className="whitespace-pre-wrap break-words font-sans text-sm leading-7 text-slate-300">
            {researchData.report || "No research report was returned."}
          </pre>
        </div>
      );
    }

    if (activeTab === "Critic Review") {
      return (
        <div className="p-5 md:p-8">
          <div className="mb-5 flex items-center gap-2">
            <ShieldCheck size={16} className="text-emerald-400" />
            <h4 className="text-sm font-semibold text-white">
              Quality Critic Evaluation
            </h4>
          </div>

          <pre className="whitespace-pre-wrap break-words font-sans text-sm leading-7 text-slate-300">
            {researchData.feedback || "No critic feedback was returned."}
          </pre>
        </div>
      );
    }

    if (activeTab === "Sources") {
      return (
        <div className="p-5 md:p-8">
          <div className="mb-5 flex items-center gap-2">
            <Globe2 size={16} className="text-cyan-400" />
            <h4 className="text-sm font-semibold text-white">
              Research Sources
            </h4>
          </div>

          {sourceUrls.length > 0 ? (
            <div className="space-y-3">
              {sourceUrls.map((url, index) => (
                <a
                  key={`${url}-${index}`}
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-start gap-3 rounded-xl border border-white/[0.07] bg-white/[0.02] p-4 transition hover:border-cyan-400/30 hover:bg-cyan-400/[0.04]"
                >
                  <Globe2
                    size={16}
                    className="mt-1 shrink-0 text-cyan-400"
                  />

                  <div className="min-w-0">
                    <p className="text-xs font-semibold text-slate-200">
                      Source {index + 1}
                    </p>

                    <p className="mt-1 break-all text-xs leading-5 text-slate-500">
                      {url}
                    </p>
                  </div>

                  <ArrowUpRight
                    size={15}
                    className="ml-auto shrink-0 text-slate-500"
                  />
                </a>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-500">
              No source URLs could be extracted from the returned data.
            </p>
          )}
        </div>
      );
    }

    return (
      <div className="space-y-8 p-5 md:p-8">
        <div>
          <h4 className="mb-4 flex items-center gap-2 text-sm font-semibold text-white">
            <Search size={15} className="text-cyan-400" />
            Search Results
          </h4>

          <pre className="whitespace-pre-wrap break-words rounded-xl border border-white/[0.07] bg-[#080d16] p-4 font-sans text-xs leading-6 text-slate-400">
            {researchData.search_results || "No search results returned."}
          </pre>
        </div>

        <div>
          <h4 className="mb-4 flex items-center gap-2 text-sm font-semibold text-white">
            <FileSearch size={15} className="text-blue-400" />
            Scraped Content
          </h4>

          <pre className="whitespace-pre-wrap break-words rounded-xl border border-white/[0.07] bg-[#080d16] p-4 font-sans text-xs leading-6 text-slate-400">
            {researchData.scraped_content || "No scraped content returned."}
          </pre>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-[#080b12] text-slate-200">
      <div className="flex min-h-screen">

        {/* SIDEBAR */}
        <aside
          className={`fixed inset-y-0 left-0 z-50 flex w-[250px] flex-col border-r border-white/[0.07] bg-[#0b101a] transition-transform duration-300 lg:static lg:translate-x-0 ${
            sidebarOpen ? "translate-x-0" : "-translate-x-full"
          }`}
        >
          <div className="flex h-[76px] items-center justify-between border-b border-white/[0.07] px-6">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-cyan-400/30 bg-cyan-400/10">
                <Network className="h-5 w-5 text-cyan-400" />
              </div>

              <div>
                <h1 className="text-[17px] font-bold tracking-[0.18em] text-white">
                  NEXUS
                </h1>

                <p className="text-[9px] tracking-[0.22em] text-slate-500">
                  INTELLIGENCE SYSTEM
                </p>
              </div>
            </div>

            <button
              onClick={() => setSidebarOpen(false)}
              className="text-slate-500 lg:hidden"
            >
              ✕
            </button>
          </div>

          <div className="px-4 py-6">
            <p className="mb-3 px-3 text-[10px] font-semibold tracking-[0.18em] text-slate-600">
              WORKSPACE
            </p>

            <button className="flex w-full items-center gap-3 rounded-xl border border-cyan-400/20 bg-cyan-400/[0.08] px-3 py-3 text-left text-sm text-cyan-300">
              <Command size={17} />
              Research Console
              <span className="ml-auto h-1.5 w-1.5 rounded-full bg-cyan-400" />
            </button>

            <button className="mt-2 flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm text-slate-500 transition hover:bg-white/[0.04] hover:text-slate-200">
              <History size={17} />
              Execution History
            </button>

            <button className="mt-2 flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm text-slate-500 transition hover:bg-white/[0.04] hover:text-slate-200">
              <FileText size={17} />
              Saved Reports
            </button>
          </div>

          <div className="mx-4 border-t border-white/[0.07]" />

          <div className="px-4 py-6">
            <p className="mb-4 px-3 text-[10px] font-semibold tracking-[0.18em] text-slate-600">
              SYSTEM
            </p>

            <div className="space-y-4 px-3">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-500">AI Engine</span>

                <span className="flex items-center gap-2 text-emerald-400">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                  Configured
                </span>
              </div>

              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-500">Web Search</span>

                <span className="flex items-center gap-2 text-emerald-400">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                  Configured
                </span>
              </div>

              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-500">API Connection</span>

                <span className="flex items-center gap-2 text-emerald-400">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                  Connected
                </span>
              </div>
            </div>
          </div>

          <div className="mt-auto border-t border-white/[0.07] p-4">
            <div className="flex items-center gap-3 rounded-xl bg-white/[0.03] p-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-cyan-500 to-blue-700 text-xs font-bold text-white">
                N
              </div>

              <div className="min-w-0 flex-1">
                <p className="text-xs font-semibold text-slate-200">
                  NEXUS Workspace
                </p>

                <p className="mt-1 text-[10px] text-slate-500">
                  Research environment
                </p>
              </div>

              <Settings2 size={16} className="text-slate-500" />
            </div>
          </div>
        </aside>

        {/* MAIN CONTENT */}
        <section className="min-w-0 flex-1">

          {/* TOP BAR */}
          <header className="flex h-[76px] items-center justify-between border-b border-white/[0.07] px-5 md:px-9">
            <div className="flex items-center gap-3">
              <button
                onClick={() => setSidebarOpen(true)}
                className="text-slate-400 lg:hidden"
              >
                <Menu size={21} />
              </button>

              <div>
                <p className="text-xs text-slate-500">
                  Workspace /{" "}
                  <span className="text-slate-300">Research Console</span>
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="hidden items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/[0.06] px-3 py-1.5 sm:flex">
                <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />

                <span className="text-[10px] tracking-wider text-emerald-400">
                  SYSTEM READY
                </span>
              </div>

              <button className="rounded-lg border border-white/[0.08] p-2 text-slate-400 hover:bg-white/[0.05]">
                <Settings2 size={17} />
              </button>
            </div>
          </header>

          {/* DASHBOARD BODY */}
          <div className="mx-auto max-w-[1450px] px-5 py-8 md:px-9 md:py-10">

            {/* HERO */}
            <div className="animate-fade-up">
              <div className="mb-4 flex items-center gap-2">
                <Sparkles size={14} className="text-cyan-400" />

                <span className="text-[10px] font-semibold tracking-[0.22em] text-cyan-400">
                  MULTI-AGENT RESEARCH ENVIRONMENT
                </span>
              </div>

              <div className="flex flex-col justify-between gap-5 md:flex-row md:items-end">
                <div>
                  <h2 className="text-3xl font-semibold tracking-tight text-white md:text-[42px]">
                    Intelligence,{" "}
                    <span className="text-cyan-400">orchestrated.</span>
                  </h2>

                  <p className="mt-3 max-w-xl text-sm leading-7 text-slate-500">
                    Deploy a coordinated team of AI agents to discover,
                    analyse, synthesise and evaluate information from across
                    the web.
                  </p>
                </div>

                <div className="flex items-center gap-2 text-xs text-slate-500">
                  <Activity size={15} className="text-cyan-400" />
                  <span>4 specialised agents</span>
                  <span className="mx-1 text-slate-700">/</span>
                  <span>1 research pipeline</span>
                </div>
              </div>
            </div>

            {/* RESEARCH INPUT */}
            <div className="glass-panel animate-fade-up mt-9 rounded-2xl p-5 md:p-7">
              <div className="mb-5 flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-semibold text-white">
                    Initiate Research
                  </h3>

                  <p className="mt-1 text-xs text-slate-500">
                    Define the subject for your AI research team.
                  </p>
                </div>

                <div className="hidden items-center gap-2 text-[10px] tracking-wider text-slate-600 sm:flex">
                  <Zap size={13} />
                  RESEARCH INPUT
                </div>
              </div>

              <div className="rounded-xl border border-white/[0.09] bg-[#080d16] p-2 transition focus-within:border-cyan-400/40">
                <textarea
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="What would you like NEXUS to investigate?"
                  rows={3}
                  disabled={isResearching}
                  className="w-full resize-none bg-transparent px-3 py-3 text-sm leading-6 text-slate-200 outline-none placeholder:text-slate-600 disabled:opacity-60"
                />

                <div className="flex flex-col justify-between gap-3 border-t border-white/[0.06] px-2 pt-3 sm:flex-row sm:items-center">
                  <div className="flex items-center gap-2 text-[10px] text-slate-600">
                    <Globe2 size={13} />
                    Web-powered research
                    <span className="text-slate-700">•</span>
                    Multi-agent workflow
                  </div>

                  <button
                    onClick={handleResearch}
                    disabled={isResearching}
                    className="flex items-center justify-center gap-2 rounded-lg bg-cyan-400 px-5 py-2.5 text-xs font-bold text-[#071017] transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {isResearching ? (
                      <>
                        <LoaderCircle size={14} className="animate-spin" />
                        Researching...
                      </>
                    ) : (
                      <>
                        Initiate Research
                        <Send size={14} />
                      </>
                    )}
                  </button>
                </div>
              </div>

              {notice && (
                <p
                  className={`mt-3 text-xs ${
                    notice.includes("successfully")
                      ? "text-emerald-400"
                      : notice.includes("Connecting")
                        ? "text-cyan-400"
                        : "text-amber-400"
                  }`}
                >
                  {notice}
                </p>
              )}

              <div className="mt-5">
                <p className="mb-3 text-[10px] font-semibold tracking-[0.16em] text-slate-600">
                  SUGGESTED RESEARCH TOPICS
                </p>

                <div className="flex flex-wrap gap-2">
                  {suggestions.map((suggestion) => (
                    <button
                      key={suggestion}
                      disabled={isResearching}
                      onClick={() => {
                        setTopic(suggestion);
                        setNotice("");
                      }}
                      className="rounded-lg border border-white/[0.07] bg-white/[0.02] px-3 py-2 text-left text-[11px] text-slate-400 transition hover:border-cyan-400/30 hover:bg-cyan-400/[0.05] hover:text-cyan-300 disabled:opacity-50"
                    >
                      {suggestion}
                      <ArrowUpRight size={11} className="ml-2 inline" />
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* AGENT PIPELINE */}
            <div className="mt-10">
              <div className="mb-5 flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-semibold text-white">
                    Agent Architecture
                  </h3>

                  <p className="mt-1 text-xs text-slate-500">
                    Four specialised agents. One coordinated workflow.
                  </p>
                </div>

                <span className="rounded-md border border-white/[0.07] px-2.5 py-1 text-[10px] text-slate-500">
                  PIPELINE V1.0
                </span>
              </div>

              <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
                {agents.map((agent, index) => {
                  const Icon = agent.icon;

                  return (
                    <div
                      key={agent.number}
                      className="glass-panel panel-hover relative overflow-hidden rounded-xl p-5"
                    >
                      <div className="mb-6 flex items-center justify-between">
                        <div
                          className={`flex h-10 w-10 items-center justify-center rounded-xl ${agent.background}`}
                        >
                          <Icon size={19} className={agent.color} />
                        </div>

                        <span className="font-mono text-[10px] tracking-widest text-slate-600">
                          {agent.number}
                        </span>
                      </div>

                      <h4 className="text-[11px] font-bold tracking-[0.08em] text-slate-200">
                        {agent.name}
                      </h4>

                      <p className="mt-2 min-h-9 text-xs leading-5 text-slate-500">
                        {agent.description}
                      </p>

                      <div className="mt-5 flex items-center gap-2 border-t border-white/[0.06] pt-3">
                        <span
                          className={`h-1.5 w-1.5 rounded-full ${
                            isResearching
                              ? "animate-pulse bg-cyan-400"
                              : researchData
                                ? "bg-emerald-400"
                                : "bg-slate-600"
                          }`}
                        />

                        <span className="text-[10px] text-slate-600">
                          {isResearching
                            ? "Pipeline running"
                            : researchData
                              ? "Execution completed"
                              : "Awaiting execution"}
                        </span>
                      </div>

                      {index < 3 && (
                        <div className="absolute right-0 top-1/2 hidden h-px w-3 translate-x-full bg-cyan-400/20 xl:block" />
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* OUTPUT AREA */}
            <div className="mt-10">
              <div className="mb-5 flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
                <div>
                  <h3 className="text-sm font-semibold text-white">
                    Research Intelligence
                  </h3>

                  <p className="mt-1 text-xs text-slate-500">
                    Your generated research and agent evaluation will appear
                    here.
                  </p>
                </div>

                <div className="flex items-center gap-2 text-[10px] text-slate-600">
                  <Clock3 size={13} />

                  {isResearching
                    ? "Research in progress"
                    : researchData
                      ? "Research session completed"
                      : "No active session"}
                </div>
              </div>

              <div className="glass-panel min-h-[290px] overflow-hidden rounded-2xl">
                {/* TABS */}
                <div className="flex gap-1 overflow-x-auto border-b border-white/[0.07] px-3 pt-3 md:px-5">
                  {tabs.map((tab) => {
                    const Icon = tab.icon;
                    const active = activeTab === tab.name;

                    return (
                      <button
                        key={tab.name}
                        onClick={() => setActiveTab(tab.name)}
                        className={`flex shrink-0 items-center gap-2 border-b-2 px-3 py-3 text-[11px] transition ${
                          active
                            ? "border-cyan-400 text-cyan-300"
                            : "border-transparent text-slate-500 hover:text-slate-300"
                        }`}
                      >
                        <Icon size={14} />
                        {tab.name}
                      </button>
                    );
                  })}
                </div>

                {/* DYNAMIC RESEARCH CONTENT */}
                <div>{renderResearchOutput()}</div>
              </div>
            </div>

            {/* FOOTER */}
            <footer className="mt-10 flex flex-col justify-between gap-3 border-t border-white/[0.06] pt-5 text-[10px] text-slate-600 sm:flex-row">
              <p>NEXUS INTELLIGENCE SYSTEM · RESEARCH ENVIRONMENT</p>

              <div className="flex items-center gap-2">
                <CheckCircle2 size={12} className="text-emerald-500" />
                Interface operational
                <span className="mx-1 text-slate-700">|</span>
                <span>v1.0.0</span>
              </div>
            </footer>

          </div>
        </section>
      </div>
    </main>
  );
}
