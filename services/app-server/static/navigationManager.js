class NavigationManager {
    static toDashboard() {
        window.location.href = '/dashboard';
    }

    static toDashboardSymbols(dashboardId) {
        window.location.href = `/dashboard/${dashboardId}/symbols`;
    }
}
