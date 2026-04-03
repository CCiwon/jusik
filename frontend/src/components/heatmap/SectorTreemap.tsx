"use client";

import { useEffect, useRef, useState } from "react";
import * as d3 from "d3";
import type { SectorItem } from "@/types";
import { heatmapColor, formatChange } from "@/lib/formatters";

interface Props {
  sectors: SectorItem[];
  title: string;
}

interface TreeNode {
  name: string;
  value: number;
  change: number | null;
  symbol?: string;
  isSector?: boolean;
  sectorName?: string;
}

export function SectorTreemap({ sectors, title }: Props) {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [tooltip, setTooltip] = useState<{
    x: number; y: number; name: string; change: number | null; symbol?: string;
  } | null>(null);

  useEffect(() => {
    if (!svgRef.current || !containerRef.current || sectors.length === 0) return;

    const width = containerRef.current.clientWidth;
    const height = 280;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();
    svg.attr("width", width).attr("height", height);

    // 데이터 구성: 섹터 → 종목 계층
    const children = sectors.map((sector) => ({
      name: sector.sector_name_ko ?? sector.sector_name,
      children: sector.instruments.map((inst) => ({
        name: inst.name,
        symbol: inst.symbol,
        value: inst.market_cap ?? 1,
        change: inst.change_percent,
        isSector: false,
        sectorName: sector.sector_name_ko ?? sector.sector_name,
      })),
    }));

    const root = d3
      .hierarchy<{ name: string; children?: TreeNode[] }>({ name: "root", children })
      .sum((d) => (d as TreeNode).value ?? 0)
      .sort((a, b) => (b.value ?? 0) - (a.value ?? 0));

    d3.treemap<{ name: string; children?: TreeNode[] }>()
      .size([width, height])
      .padding(2)
      .paddingTop(18)(root);

    // 섹터 그룹 (상위 노드)
    const sectorGroups = svg
      .selectAll("g.sector")
      .data(root.children ?? [])
      .enter()
      .append("g")
      .attr("class", "sector");

    sectorGroups
      .append("rect")
      .attr("x", (d) => (d as d3.HierarchyRectangularNode<unknown>).x0)
      .attr("y", (d) => (d as d3.HierarchyRectangularNode<unknown>).y0)
      .attr("width", (d) => {
        const n = d as d3.HierarchyRectangularNode<unknown>;
        return Math.max(0, n.x1 - n.x0);
      })
      .attr("height", (d) => {
        const n = d as d3.HierarchyRectangularNode<unknown>;
        return Math.max(0, n.y1 - n.y0);
      })
      .attr("fill", "transparent")
      .attr("stroke", "#1e293b")
      .attr("stroke-width", 1);

    sectorGroups
      .append("text")
      .attr("x", (d) => (d as d3.HierarchyRectangularNode<unknown>).x0 + 4)
      .attr("y", (d) => (d as d3.HierarchyRectangularNode<unknown>).y0 + 13)
      .attr("font-size", "10px")
      .attr("fill", "#94a3b8")
      .text((d) => {
        const n = d as d3.HierarchyRectangularNode<{ name: string }>;
        const w = n.x1 - n.x0;
        return w > 40 ? n.data.name : "";
      });

    // 종목 셀 (리프 노드)
    const leaves = svg
      .selectAll("g.leaf")
      .data(root.leaves())
      .enter()
      .append("g")
      .attr("class", "leaf")
      .style("cursor", "pointer");

    leaves
      .append("rect")
      .attr("x", (d) => (d as d3.HierarchyRectangularNode<unknown>).x0 + 1)
      .attr("y", (d) => (d as d3.HierarchyRectangularNode<unknown>).y0 + 1)
      .attr("width", (d) => {
        const n = d as d3.HierarchyRectangularNode<unknown>;
        return Math.max(0, n.x1 - n.x0 - 2);
      })
      .attr("height", (d) => {
        const n = d as d3.HierarchyRectangularNode<unknown>;
        return Math.max(0, n.y1 - n.y0 - 2);
      })
      .attr("rx", 2)
      .attr("fill", (d) => heatmapColor((d.data as TreeNode).change))
      .attr("stroke", "#0f1117")
      .attr("stroke-width", 0.5)
      .on("mouseenter", (event, d) => {
        const node = d as d3.HierarchyRectangularNode<TreeNode>;
        const rect = (event.target as SVGRectElement).getBoundingClientRect();
        const containerRect = containerRef.current!.getBoundingClientRect();
        setTooltip({
          x: rect.left - containerRect.left + rect.width / 2,
          y: rect.top - containerRect.top - 8,
          name: node.data.name,
          change: node.data.change,
          symbol: node.data.symbol,
        });
      })
      .on("mouseleave", () => setTooltip(null));

    leaves
      .append("text")
      .attr("x", (d) => {
        const n = d as d3.HierarchyRectangularNode<unknown>;
        return n.x0 + (n.x1 - n.x0) / 2;
      })
      .attr("y", (d) => {
        const n = d as d3.HierarchyRectangularNode<unknown>;
        return n.y0 + (n.y1 - n.y0) / 2 + 4;
      })
      .attr("text-anchor", "middle")
      .attr("font-size", "10px")
      .attr("fill", "rgba(255,255,255,0.9)")
      .attr("pointer-events", "none")
      .text((d) => {
        const n = d as d3.HierarchyRectangularNode<TreeNode>;
        const w = n.x1 - n.x0;
        const h = n.y1 - n.y0;
        if (w < 30 || h < 20) return "";
        return n.data.symbol ?? n.data.name;
      });
  }, [sectors]);

  return (
    <div className="bg-slate-900 rounded-lg border border-slate-800 p-3">
      <h3 className="text-slate-300 text-sm font-semibold mb-2">{title}</h3>
      <div ref={containerRef} className="relative w-full">
        <svg ref={svgRef} className="w-full" />
        {tooltip && (
          <div
            className="absolute z-10 bg-slate-800 border border-slate-700 rounded px-2.5 py-1.5 text-xs pointer-events-none shadow-lg"
            style={{ left: tooltip.x, top: tooltip.y, transform: "translate(-50%, -100%)" }}
          >
            <div className="text-slate-200 font-medium">{tooltip.name}</div>
            {tooltip.symbol && <div className="text-slate-400">{tooltip.symbol}</div>}
            <div className={tooltip.change != null && tooltip.change >= 0 ? "text-green-400" : "text-red-400"}>
              {formatChange(tooltip.change)}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
