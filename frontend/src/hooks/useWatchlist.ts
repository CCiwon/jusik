"use client";

import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import type { WatchlistResponse, WatchlistSortKey, MarketFilter } from "@/types";

interface UseWatchlistOptions {
  market?: MarketFilter;
  sort?: WatchlistSortKey;
}

export function useWatchlist({ market = "all", sort = "display_order" }: UseWatchlistOptions = {}) {
  return useQuery<WatchlistResponse>({
    queryKey: ["watchlist", market, sort],
    queryFn: async () => {
      const { data } = await apiClient.get<WatchlistResponse>("/watchlist", {
        params: { market, sort },
      });
      return data;
    },
    refetchInterval: 60_000,
    staleTime: 30_000,
  });
}
