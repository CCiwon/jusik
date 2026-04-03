"use client";

import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import type { SummaryBarResponse } from "@/types";

export function useSummaryBar() {
  return useQuery<SummaryBarResponse>({
    queryKey: ["summary-bar"],
    queryFn: async () => {
      const { data } = await apiClient.get<SummaryBarResponse>("/summary-bar");
      return data;
    },
    refetchInterval: 60_000,
    staleTime: 30_000,
  });
}
