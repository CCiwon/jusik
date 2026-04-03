"use client";

import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import type { EventsResponse, EventRange, EventCountry, EventCategory } from "@/types";

interface UseEventsOptions {
  range?: EventRange;
  country?: EventCountry;
  category?: EventCategory;
}

export function useEvents({
  range = "week",
  country = "all",
  category = "all",
}: UseEventsOptions = {}) {
  return useQuery<EventsResponse>({
    queryKey: ["events", range, country, category],
    queryFn: async () => {
      const { data } = await apiClient.get<EventsResponse>("/events", {
        params: { range, country, category },
      });
      return data;
    },
    refetchInterval: 30 * 60_000,
    staleTime: 15 * 60_000,
  });
}
