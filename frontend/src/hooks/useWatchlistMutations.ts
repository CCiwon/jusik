"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";

export function useToggleWatchlist() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ marketType, symbol }: { marketType: string; symbol: string }) => {
      const { data } = await apiClient.patch(`/watchlist/${marketType}/${symbol}`);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["watchlist"] });
    },
  });
}

export function useSearchInstruments(q: string, market: string) {
  return {
    search: async () => {
      if (!q.trim()) return [];
      const { data } = await apiClient.get("/instruments/search", {
        params: { q, market },
      });
      return data;
    },
  };
}
