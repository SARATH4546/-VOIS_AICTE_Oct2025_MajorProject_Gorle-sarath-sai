/**
 * Netflix Analysis Dashboard - JavaScript Engine
 * Advanced interactive functionality for the analytics platform
 */

class NetflixDashboard {
    constructor() {
        this.charts = {};
        this.currentData = null;
        this.isLoading = false;
        this.retryAttempts = {};
        this.maxRetries = 3;
        
        // Initialize dashboard
        this.init();
    }
    
    init() {
        console.log('🎬 Netflix Dashboard initializing...');
        
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupDashboard());
        } else {
            this.setupDashboard();
        }
    }
    
    setupDashboard() {
        console.log('📊 Setting up dashboard components...');
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Load charts if on dashboard page
        if (this.isDashboardPage()) {
            this.loadAllCharts();
        }
        
        // Setup auto-refresh
        this.setupAutoRefresh();
        
        // Setup keyboard shortcuts
        this.setupKeyboardShortcuts();
        
        console.log('✅ Dashboard setup complete!');
    }
    
    setupEventListeners() {
        // Retry buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('retry-chart-btn')) {
                const chartType = e.target.dataset.chart;
                this.retryChart(chartType);
            }
        });
        
        // Refresh button
        const refreshBtn = document.getElementById('refresh-dashboard');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refreshAllCharts();
            });
        }
        
        // Export buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('export-chart-btn')) {
                const chartType = e.target.dataset.chart;
                const format = e.target.dataset.format || 'png';
                this.exportChart(chartType, format);
            }
        });
        
        // Fullscreen chart buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('fullscreen-chart-btn')) {
                const chartType = e.target.dataset.chart;
                this.toggleFullscreen(chartType);
            }
        });
    }
    
    isDashboardPage() {
        return window.location.pathname.includes('/dashboard') || 
               document.getElementById('dashboard-content') !== null;
    }
    
    loadAllCharts() {
        console.log('📈 Loading all dashboard charts...');
        
        const chartConfigs = [
            { endpoint: '/api/temporal-chart', elementId: 'temporal-chart', name: 'Content Growth Over Time' },
            { endpoint: '/api/content-mix-chart', elementId: 'content-mix-chart', name: 'Content Mix' },
            { endpoint: '/api/genre-chart', elementId: 'genre-chart', name: 'Top Genres' },
            { endpoint: '/api/geographic-chart', elementId: 'geographic-chart', name: 'Top Countries' }
        ];
        
        // Load charts with staggered delay for better UX
        chartConfigs.forEach((config, index) => {
            setTimeout(() => {
                this.loadChart(config.endpoint, config.elementId, config.name);
            }, index * 200);
        });
    }
    
    async loadChart(endpoint, elementId, chartName) {
        const element = document.getElementById(elementId);
        if (!element) {
            console.warn(`⚠️ Chart element not found: ${elementId}`);
            return;
        }
        
        // Show loading state
        this.showLoadingState(elementId, chartName);
        
        try {
            console.log(`📊 Loading ${chartName}...`);
            
            const response = await fetch(endpoint, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                timeout: 15000 // 15 second timeout
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            if (data.chart) {
                const chartData = JSON.parse(data.chart);
                await this.renderChart(elementId, chartData, chartName);
                console.log(`✅ ${chartName} loaded successfully`);
                
                // Reset retry count on success
                this.retryAttempts[elementId] = 0;
                
            } else if (data.error) {
                throw new Error(data.error);
            } else {
                throw new Error('Invalid response format');
            }
            
        } catch (error) {
            console.error(`❌ Error loading ${chartName}:`, error);
            this.showErrorState(elementId, chartName, error.message);
        }
    }
    
    async renderChart(elementId, chartData, chartName) {
        try {
            // Enhance chart configuration
            const enhancedConfig = {
                ...chartData,
                config: {
                    responsive: true,
                    displayModeBar: true,
                    modeBarButtonsToAdd: [
                        {
                            name: 'Export PNG',
                            icon: Plotly.Icons.camera,
                            click: () => this.exportChart(elementId, 'png')
                        }
                    ],
                    toImageButtonOptions: {
                        format: 'png',
                        filename: `netflix_${chartName.toLowerCase().replace(/\s+/g, '_')}`,
                        height: 500,
                        width: 800,
                        scale: 2
                    }
                }
            };
            
            // Apply Netflix theme
            if (enhancedConfig.layout) {
                enhancedConfig.layout = {
                    ...enhancedConfig.layout,
                    font: { family: 'Arial, sans-serif', size: 12 },
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    plot_bgcolor: 'rgba(0,0,0,0)',
                    margin: { t: 60, r: 40, b: 80, l: 80 }
                };
            }
            
            // Render with Plotly
            await Plotly.newPlot(
                elementId, 
                enhancedConfig.data, 
                enhancedConfig.layout, 
                enhancedConfig.config
            );
            
            // Store chart reference
            this.charts[elementId] = {
                data: enhancedConfig.data,
                layout: enhancedConfig.layout,
                config: enhancedConfig.config,
                name: chartName
            };
            
            // Add resize listener
            this.setupChartResize(elementId);
            
            // Add animation
            this.animateChart(elementId);
            
        } catch (error) {
            console.error(`❌ Error rendering chart ${chartName}:`, error);
            throw error;
        }
    }
    
    showLoadingState(elementId, chartName) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="loading">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <span class="ms-2">Loading ${chartName}...</span>
                </div>
            `;
        }
    }
    
    showErrorState(elementId, chartName, errorMessage) {
        const element = document.getElementById(elementId);
        const retryCount = this.retryAttempts[elementId] || 0;
        
        if (element) {
            element.innerHTML = `
                <div class="alert alert-danger">
                    <h6><i class="fas fa-exclamation-triangle"></i> Failed to load ${chartName}</h6>
                    <p class="mb-2">Error: ${errorMessage}</p>
                    ${retryCount < this.maxRetries ? `
                        <button class="btn btn-sm btn-outline-danger retry-chart-btn" 
                                data-chart="${elementId}" 
                                data-name="${chartName}">
                            <i class="fas fa-redo"></i> Retry (${retryCount + 1}/${this.maxRetries})
                        </button>
                    ` : `
                        <p class="text-muted small mb-0">
                            Maximum retry attempts reached. Please refresh the page.
                        </p>
                    `}
                </div>
            `;
        }
    }
    
    retryChart(elementId) {
        const retryCount = this.retryAttempts[elementId] || 0;
        
        if (retryCount >= this.maxRetries) {
            console.warn(`⚠️ Maximum retries reached for ${elementId}`);
            return;
        }
        
        this.retryAttempts[elementId] = retryCount + 1;
        
        // Find the chart configuration and retry
        const chartConfigs = [
            { endpoint: '/api/temporal-chart', elementId: 'temporal-chart', name: 'Content Growth Over Time' },
            { endpoint: '/api/content-mix-chart', elementId: 'content-mix-chart', name: 'Content Mix' },
            { endpoint: '/api/genre-chart', elementId: 'genre-chart', name: 'Top Genres' },
            { endpoint: '/api/geographic-chart', elementId: 'geographic-chart', name: 'Top Countries' }
        ];
        
        const config = chartConfigs.find(c => c.elementId === elementId);
        if (config) {
            console.log(`🔄 Retrying ${config.name} (attempt ${retryCount + 1})`);
            this.loadChart(config.endpoint, config.elementId, config.name);
        }
    }
    
    refreshAllCharts() {
        console.log('🔄 Refreshing all charts...');
        
        // Reset retry attempts
        this.retryAttempts = {};
        
        // Reload all charts
        this.loadAllCharts();
        
        // Show feedback
        this.showToast('Charts refreshed successfully!', 'success');
    }
    
    setupChartResize(elementId) {
        let resizeTimeout;
        
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                if (this.charts[elementId]) {
                    Plotly.Plots.resize(elementId);
                }
            }, 250);
        });
    }
    
    animateChart(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                element.style.transition = 'all 0.6s ease';
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, 100);
        }
    }
    
    exportChart(elementId, format = 'png') {
        if (this.charts[elementId]) {
            const chartName = this.charts[elementId].name || 'chart';
            const filename = `netflix_${chartName.toLowerCase().replace(/\s+/g, '_')}.${format}`;
            
            Plotly.toImage(elementId, {
                format: format,
                width: 1200,
                height: 700,
                scale: 2
            }).then(dataUrl => {
                const link = document.createElement('a');
                link.download = filename;
                link.href = dataUrl;
                link.click();
                
                this.showToast(`Chart exported as ${filename}`, 'success');
            }).catch(error => {
                console.error('Export failed:', error);
                this.showToast('Export failed. Please try again.', 'error');
            });
        }
    }
    
    toggleFullscreen(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            if (element.requestFullscreen) {
                element.requestFullscreen();
            } else if (element.webkitRequestFullscreen) {
                element.webkitRequestFullscreen();
            } else if (element.mozRequestFullScreen) {
                element.mozRequestFullScreen();
            }
        }
    }
    
    setupAutoRefresh() {
        // Auto-refresh every 5 minutes if enabled
        const autoRefreshEnabled = localStorage.getItem('netflix-auto-refresh') === 'true';
        
        if (autoRefreshEnabled) {
            setInterval(() => {
                console.log('🔄 Auto-refreshing charts...');
                this.refreshAllCharts();
            }, 5 * 60 * 1000); // 5 minutes
        }
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+R or F5: Refresh charts
            if ((e.ctrlKey && e.key === 'r') || e.key === 'F5') {
                if (this.isDashboardPage()) {
                    e.preventDefault();
                    this.refreshAllCharts();
                }
            }
            
            // Ctrl+E: Export all charts
            if (e.ctrlKey && e.key === 'e') {
                if (this.isDashboardPage()) {
                    e.preventDefault();
                    this.exportAllCharts();
                }
            }
        });
    }
    
    exportAllCharts() {
        const chartIds = Object.keys(this.charts);
        let exportCount = 0;
        
        chartIds.forEach((chartId, index) => {
            setTimeout(() => {
                this.exportChart(chartId, 'png');
                exportCount++;
                
                if (exportCount === chartIds.length) {
                    this.showToast(`All ${exportCount} charts exported!`, 'success');
                }
            }, index * 500); // Stagger exports
        });
    }
    
    showToast(message, type = 'info') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `alert alert-${type === 'error' ? 'danger' : type} position-fixed`;
        toast.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        `;
        toast.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'}"></i>
            ${message}
        `;
        
        document.body.appendChild(toast);
        
        // Animate in
        setTimeout(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }
    
    // Public API methods
    getChartData(elementId) {
        return this.charts[elementId] || null;
    }
    
    updateChart(elementId, newData, newLayout = null) {
        if (this.charts[elementId]) {
            const update = { data: newData };
            if (newLayout) update.layout = newLayout;
            
            Plotly.react(elementId, newData, newLayout || this.charts[elementId].layout);
            
            // Update stored reference
            this.charts[elementId].data = newData;
            if (newLayout) this.charts[elementId].layout = newLayout;
        }
    }
    
    addCustomChart(elementId, chartData, chartName) {
        this.renderChart(elementId, chartData, chartName);
    }
}

// Utility Functions
class ChartUtils {
    static formatNumber(num) {
        if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
        if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
        return num.toString();
    }
    
    static getNetflixColors() {
        return {
            primary: '#E50914',
            secondary: '#564D4D',
            success: '#28a745',
            warning: '#ffc107',
            info: '#17a2b8',
            light: '#f8f9fa',
            dark: '#221F1F'
        };
    }
    
    static createGradient(color1, color2, steps = 10) {
        const colors = [];
        for (let i = 0; i < steps; i++) {
            const ratio = i / (steps - 1);
            colors.push(this.interpolateColor(color1, color2, ratio));
        }
        return colors;
    }
    
    static interpolateColor(color1, color2, ratio) {
        const hex = (color) => parseInt(color.replace('#', ''), 16);
        const r1 = (hex(color1) >> 16) & 255;
        const g1 = (hex(color1) >> 8) & 255;
        const b1 = hex(color1) & 255;
        
        const r2 = (hex(color2) >> 16) & 255;
        const g2 = (hex(color2) >> 8) & 255;
        const b2 = hex(color2) & 255;
        
        const r = Math.round(r1 + (r2 - r1) * ratio);
        const g = Math.round(g1 + (g2 - g1) * ratio);
        const b = Math.round(b1 + (b2 - b1) * ratio);
        
        return `#${((r << 16) | (g << 8) | b).toString(16).padStart(6, '0')}`;
    }
}

// Initialize dashboard when script loads
let netflixDashboard;
if (typeof window !== 'undefined') {
    netflixDashboard = new NetflixDashboard();
    
    // Make utilities available globally
    window.ChartUtils = ChartUtils;
    window.NetflixDashboard = netflixDashboard;
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { NetflixDashboard, ChartUtils };
}