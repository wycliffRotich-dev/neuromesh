import { useEffect, useState } from "react";

import { fetchNodes } from "../api/dashboard";
import type { NodeResponse } from "../api/types";

export function useNodes() {
  const [nodes, setNodes] = useState<NodeResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadNodes() {
      try {
        const response = await fetchNodes();
        setNodes(response.nodes);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Unknown error");
        }
      } finally {
        setLoading(false);
      }
    }

    void loadNodes();
  }, []);

  return {
    nodes,
    loading,
    error,
  };
}
