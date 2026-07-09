export interface DashboardMetric {
    title: string;
    value: string;
    delta: string;
}

export interface DashboardResponse {
    metrics: DashboardMetric[];
}