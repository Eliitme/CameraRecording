"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import React from "react";

const MainLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <QueryClientProvider
      client={
        new QueryClient({
          defaultOptions: {
            queries: {
              refetchOnWindowFocus: false,
            },
          },
        })
      }
    >
      {children}
    </QueryClientProvider>
  );
};

export default MainLayout;
