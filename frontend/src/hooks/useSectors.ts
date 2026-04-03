"use client";

import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import type { HeatmapResponse } from "@/types";

export function useSectors() {
  return useQuery<HeatmapResponse>({
    queryKey: ["sectors"],
    queryFn: async () => {
      const { data } = await apiClient.get<HeatmapResponse>("/sectors/heatmap");
      return data;
    },
    refetchInterval: 5 * 60_000,
    staleTime: 3 * 60_000,
  });
}
