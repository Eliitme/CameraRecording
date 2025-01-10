"use client";

import getTreeAPI from "@/api/getTree";
import { useQuery } from "@tanstack/react-query";

export default function useGetTree() {
  const key = ["tree"];

  const { data, isLoading } = useQuery({
    queryKey: key,
    queryFn: async () => {
      const data = await getTreeAPI();

      return data;
    },
    refetchInterval: 60 * 60 * 1000,
  });

  return { data, isLoading };
}
