"use client";

import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import type { OpeningBriefResponse } from "@/types";

export function useOpeningBrief() {
  return useQuery<OpeningBriefResponse>({
    queryKey: ["ai", "opening-brief"],
    queryFn: async () => {
      const { data } = await apiClient.get<OpeningBriefResponse>("/ai/opening-brief");
      return data;
    },
    refetchInterval: 5 * 60_000,
    staleTime: 3 * 60_000,
  });
}
