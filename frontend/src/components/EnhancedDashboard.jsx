import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
    BarChart, Bar, LineChart, Line, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
    XAxis, YAxis, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import {
    TrendingUp, AlertTriangle, CheckCircle, DollarSign,
    Activity, Target, Award, FileText, Download
} from 'lucide-react';
import { useTranslation } from '../context/TranslationContext';

const EnhancedDashboard = ({ data, businessProfile }) => {
    const { t } = useTranslation();
    const [activeTab, setActiveTab] = useState('overview');

    if (!data) return null;

    const {
        health_score,
        creditworthiness_score,
        risk_level,
        insights,
        recommendations,
        metrics,
        benchmark_comparison,
        product_recommendations,
        tax_compliance,
        cash_flow_forecast
    } = data;

    const scoreColor = health_score >= 80 ? '#22c55e' : health_score >= 50 ? '#eab308' : '#ef4444';
    const riskColor = risk_level === 'Low' ? '#22c55e' : risk_level === 'Moderate' ? '#eab308' : '#ef4444';

    const tabs = [
        { id: 'overview', label: t('dashboard.overview'), icon: Activity },
        { id: 'metrics', label: t('dashboard.detailedMetrics'), icon: Target },
        { id: 'forecast', label: t('dashboard.cashFlow'), icon: TrendingUp },
        { id: 'benchmark', label: t('dashboard.benchmarking'), icon: Award },
        { id: 'products', label: t('dashboard.recommendations'), icon: DollarSign },
        { id: 'tax', label: t('dashboard.taxCompliance'), icon: FileText }
    ];

    // Prepare chart data
    const metricsChartData = [
        { name: t('dashboard.currentRatio') || 'Current Ratio', value: metrics.liquidity.current_ratio, benchmark: 1.5 },
        { name: t('dashboard.profitMargin') || 'Profit Margin', value: metrics.profitability.net_profit_margin, benchmark: 10 },
        { name: t('dashboard.roe') || 'ROE', value: metrics.profitability.return_on_equity, benchmark: 15 },
        { name: t('dashboard.assetTurnover') || 'Asset Turnover', value: metrics.efficiency.asset_turnover, benchmark: 1.5 }
    ];

    const radarData = benchmark_comparison?.metrics_comparison ? Object.keys(benchmark_comparison.metrics_comparison).map(key => ({
        // Try to translate the key if it exists in dashboard metrics, otherwise format it
        metric: t(`dashboard.${key}`) !== `dashboard.${key}` ? t(`dashboard.${key}`) : key.replace(/_/g, ' ').toUpperCase(),
        value: benchmark_comparison.metrics_comparison[key].percentile,
        fullMark: 100
    })) : [];

    const handleExport = () => {
        window.print();
    };

    return (
        <>
            <motion.div
                className="no-print"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
            >
                {/* Tabs */}
                <div style={{
                    display: 'flex',
                    gap: '8px',
                    marginBottom: '24px',
                    overflowX: 'auto',
                    borderBottom: '1px solid var(--glass-border)',
                    paddingBottom: '8px'
                }}>
                    {tabs.map(tab => {
                        const Icon = tab.icon;
                        return (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className="btn"
                                style={{
                                    background: activeTab === tab.id ? 'var(--accent-color)' : 'transparent',
                                    color: activeTab === tab.id ? '#fff' : 'var(--text-secondary)',
                                    padding: '10px 16px',
                                    fontSize: '0.9rem',
                                    whiteSpace: 'nowrap'
                                }}
                            >
                                <Icon size={16} style={{ marginRight: '6px', verticalAlign: '-2px' }} />
                                {tab.label}
                            </button>
                        );
                    })}
                </div>

                {/* Overview Tab */}
                {activeTab === 'overview' && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                        {/* Score Cards */}
                        <div className="grid grid-2">
                            <motion.div className="card metric-card" whileHover={{ scale: 1.02 }}>
                                <div className="metric-label">{t('dashboard.financialHealthScore')}</div>
                                <div className="metric-value" style={{ color: scoreColor }}>{health_score}/100</div>
                                <div style={{ color: riskColor, fontWeight: 500, marginTop: '8px' }}>
                                    {risk_level} {t('dashboard.risk')}
                                </div>
                            </motion.div>

                            <motion.div className="card metric-card" whileHover={{ scale: 1.02 }}>
                                <div className="metric-label">{t('dashboard.creditworthinessScore')}</div>
                                <div className="metric-value" style={{ color: scoreColor }}>{creditworthiness_score}/100</div>
                                {benchmark_comparison && (
                                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '8px' }}>
                                        {benchmark_comparison.overall_performance}
                                    </div>
                                )}
                            </motion.div>
                        </div>

                        {/* Key Metrics Visualization */}
                        <div className="card">
                            <h3>{t('dashboard.keyFinancialMetrics')}</h3>
                            <div style={{ width: '100%', height: 250, marginTop: '16px' }}>
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={metricsChartData}>
                                        <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                                        <YAxis tick={{ fill: '#94a3b8' }} />
                                        <Tooltip
                                            contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }}
                                            labelStyle={{ color: '#f8fafc' }}
                                        />
                                        <Bar dataKey="value" fill="#38bdf8" radius={[8, 8, 0, 0]} />
                                        <Bar dataKey="benchmark" fill="#94a3b8" radius={[8, 8, 0, 0]} opacity={0.3} />
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        {/* Insights & Recommendations */}
                        <div className="grid grid-2">
                            <div className="card">
                                <h3>
                                    <TrendingUp size={20} style={{ marginRight: 8, verticalAlign: 'middle' }} />
                                    {t('dashboard.aiInsights')}
                                </h3>
                                <ul style={{ paddingLeft: 20, marginTop: 16 }}>
                                    {insights.map((insight, idx) => (
                                        <li key={idx} style={{ marginBottom: 12, lineHeight: 1.5 }}>
                                            {insight}
                                        </li>
                                    ))}
                                </ul>
                            </div>

                            <div className="card">
                                <h3>
                                    <CheckCircle size={20} style={{ marginRight: 8, verticalAlign: 'middle' }} />
                                    {t('dashboard.strategicRecommendations')}
                                </h3>
                                <ul style={{ paddingLeft: 20, marginTop: 16 }}>
                                    {recommendations.map((rec, idx) => (
                                        <li key={idx} style={{ marginBottom: 12, lineHeight: 1.5 }}>
                                            {rec}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>
                )}

                {/* Detailed Metrics Tab */}
                {activeTab === 'metrics' && (
                    <div className="grid grid-2">
                        {Object.keys(metrics).map(category => (
                            <div key={category} className="card">
                                <h3 style={{ textTransform: 'capitalize', marginBottom: '16px' }}>
                                    {category.replace(/_/g, ' ')}
                                </h3>
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                    {Object.entries(metrics[category]).map(([key, value]) => (
                                        <div key={key} style={{
                                            display: 'flex',
                                            justifyContent: 'space-between',
                                            padding: '8px 12px',
                                            background: 'var(--bg-primary)',
                                            borderRadius: '6px'
                                        }}>
                                            <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                                                {key.replace(/_/g, ' ').toUpperCase()}
                                            </span>
                                            <span style={{ fontWeight: 600, color: 'var(--accent-color)' }}>
                                                {typeof value === 'number' ? value.toFixed(2) : value}
                                            </span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {/* Cash Flow Forecast Tab */}
                {activeTab === 'forecast' && cash_flow_forecast && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                        <div className="card">
                            <h3>{t('dashboard.cashFlowProjection')}</h3>
                            <div style={{ width: '100%', height: 300, marginTop: '16px' }}>
                                <ResponsiveContainer width="100%" height="100%">
                                    <LineChart data={cash_flow_forecast.monthly_projections}>
                                        <XAxis dataKey="month" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                                        <YAxis tick={{ fill: '#94a3b8' }} />
                                        <Tooltip
                                            contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }}
                                        />
                                        <Legend />
                                        <Line type="monotone" dataKey="revenue" stroke="#38bdf8" strokeWidth={2} />
                                        <Line type="monotone" dataKey="net_income" stroke="#22c55e" strokeWidth={2} />
                                        <Line type="monotone" dataKey="net_cash_flow" stroke="#f472b6" strokeWidth={2} />
                                    </LineChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        <div className="card">
                            <h3>{t('dashboard.workingCapitalRecs')}</h3>
                            <ul style={{ paddingLeft: 20, marginTop: 16 }}>
                                {cash_flow_forecast.working_capital_recommendations.map((rec, idx) => (
                                    <li key={idx} style={{ marginBottom: 12, lineHeight: 1.5 }}>
                                        {rec}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                )}

                {/* Benchmark Tab */}
                {activeTab === 'benchmark' && benchmark_comparison && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                        <div className="card">
                            <h3>{t('dashboard.industryPerformance')}</h3>
                            <div style={{ textAlign: 'center', margin: '16px 0' }}>
                                <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--accent-color)' }}>
                                    {benchmark_comparison.percentile_rank}th
                                </div>
                                <div style={{ color: 'var(--text-secondary)' }}>{t('dashboard.percentile')}</div>
                                <div style={{ marginTop: '8px', fontWeight: 500 }}>
                                    {benchmark_comparison.overall_performance}
                                </div>
                            </div>

                            {radarData.length > 0 && (
                                <div style={{ width: '100%', height: 300 }}>
                                    <ResponsiveContainer width="100%" height="100%">
                                        <RadarChart data={radarData}>
                                            <PolarGrid stroke="#334155" />
                                            <PolarAngleAxis dataKey="metric" tick={{ fill: '#94a3b8', fontSize: 10 }} />
                                            <PolarRadiusAxis tick={{ fill: '#94a3b8' }} />
                                            <Radar name={t('dashboard.yourBusiness') || "Your Business"} dataKey="value" stroke="#38bdf8" fill="#38bdf8" fillOpacity={0.6} />
                                        </RadarChart>
                                    </ResponsiveContainer>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {/* Products Tab */}
                {activeTab === 'products' && product_recommendations && (
                    <div className="grid grid-2">
                        {product_recommendations.slice(0, 4).map((product, idx) => (
                            <div key={idx} className="card" style={{
                                border: product.eligible ? '1px solid var(--accent-color)' : '1px solid var(--glass-border)'
                            }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '12px' }}>
                                    <h4 style={{ margin: 0 }}>{product.name}</h4>
                                    {product.eligible && (
                                        <span style={{
                                            background: 'var(--success)',
                                            color: '#fff',
                                            padding: '4px 8px',
                                            borderRadius: '12px',
                                            fontSize: '0.75rem',
                                            fontWeight: 600
                                        }}>
                                            {t('dashboard.eligible')}
                                        </span>
                                    )}
                                </div>
                                <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '8px' }}>
                                    {product.provider} • {product.type}
                                </div>
                                <p style={{ fontSize: '0.9rem', lineHeight: 1.5, marginBottom: '12px' }}>
                                    {product.description}
                                </p>
                                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                                    <div>{t('dashboard.interestRate')}: <strong>{product.interest_rate}</strong></div>
                                    <div>{t('dashboard.tenure')}: <strong>{product.tenure}</strong></div>
                                </div>
                                <div style={{
                                    marginTop: '12px',
                                    padding: '8px',
                                    background: 'var(--bg-primary)',
                                    borderRadius: '6px',
                                    fontSize: '0.85rem'
                                }}>
                                    {product.reason}
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {/* Tax Compliance Tab */}
                {activeTab === 'tax' && tax_compliance && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                        <div className="grid grid-2">
                            <div className="card">
                                <h3>{t('dashboard.gstCompliance')}</h3>
                                <div style={{ marginTop: '16px' }}>
                                    <div style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '8px',
                                        marginBottom: '12px'
                                    }}>
                                        {tax_compliance.gst_status.compliance_status === 'Compliant' ? (
                                            <CheckCircle size={20} color="#22c55e" />
                                        ) : (
                                            <AlertTriangle size={20} color="#ef4444" />
                                        )}
                                        <span style={{ fontWeight: 600 }}>
                                            {tax_compliance.gst_status.compliance_status}
                                        </span>
                                    </div>
                                    <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                                        <div>{t('dashboard.filingFrequency')}: <strong>{tax_compliance.gst_status.filing_frequency}</strong></div>
                                        <div>{t('dashboard.applicableRate')}: <strong>{tax_compliance.gst_status.applicable_rate}%</strong></div>
                                    </div>
                                </div>
                            </div>

                            <div className="card">
                                <h3>{t('dashboard.incomeTaxEstimate')}</h3>
                                <div style={{ marginTop: '16px', fontSize: '0.9rem' }}>
                                    <div style={{ marginBottom: '8px' }}>
                                        {t('dashboard.taxableIncome')}: <strong>₹{tax_compliance.income_tax_estimate.taxable_income.toLocaleString()}</strong>
                                    </div>
                                    <div style={{ marginBottom: '8px' }}>
                                        {t('dashboard.taxRate')}: <strong>{tax_compliance.income_tax_estimate.applicable_rate}</strong>
                                    </div>
                                    <div style={{ fontSize: '1.1rem', color: 'var(--accent-color)', fontWeight: 600 }}>
                                        {t('dashboard.estimatedTax')}: ₹{tax_compliance.income_tax_estimate.estimated_tax_liability.toLocaleString()}
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="card">
                            <h3>{t('dashboard.taxOptimizationTips')}</h3>
                            <ul style={{ paddingLeft: 20, marginTop: 16 }}>
                                {tax_compliance.tax_optimization_tips.map((tip, idx) => (
                                    <li key={idx} style={{ marginBottom: 12, lineHeight: 1.5 }}>
                                        {tip}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                )}

                {/* Export Button */}
                <div style={{ marginTop: '32px', textAlign: 'center' }}>
                    <button
                        onClick={handleExport}
                        className="btn btn-primary"
                    >
                        <Download size={18} style={{ marginRight: '8px', verticalAlign: '-3px' }} />
                        {t('dashboard.exportReport')}
                    </button>
                </div>
            </motion.div>

            {/* Print Only Report Template (In Clear English) */}
            <div id="report-print-only" style={{ padding: '20px', backgroundColor: 'white', color: 'black' }}>
                <div style={{ borderBottom: '3px solid #38bdf8', paddingBottom: '20px', marginBottom: '30px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                        <h1 style={{ fontSize: '28px', margin: 0, color: '#0f172a' }}>Financial Health Assessment Report</h1>
                        <p style={{ margin: '5px 0 0 0', color: '#64748b' }}>Generated on {new Date().toLocaleDateString()} • Confidential</p>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                        <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#38bdf8' }}>FinHealth AI</div>
                        <div style={{ fontSize: '12px', color: '#94a3b8' }}>Business Intelligence Platform</div>
                    </div>
                </div>

                <div style={{ marginBottom: '30px', breakAfter: 'page' }}>
                    <h2 style={{ fontSize: '18px', borderBottom: '1px solid #e2e8f0', paddingBottom: '8px', marginBottom: '15px' }}>Business Summary</h2>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                        <div><strong>Business Name:</strong> {businessProfile?.name || 'Valued Client'}</div>
                        <div><strong>Industry Sector:</strong> {businessProfile?.industry || 'Services'}</div>
                        <div><strong>Business Type:</strong> {businessProfile?.business_type?.replace('_', ' ') || 'SME'}</div>
                        <div><strong>Operational Status:</strong> Active</div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '30px' }}>
                        <div className="card" style={{ padding: '20px', border: '1px solid #e2e8f0', textAlign: 'center' }}>
                            <div style={{ fontSize: '12px', color: '#64748b', textTransform: 'uppercase', marginBottom: '10px' }}>Financial Health Score</div>
                            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#22c55e' }}>{health_score}/100</div>
                            <p style={{ fontSize: '14px', margin: '10px 0 0 0' }}>Overall stability and performance rating.</p>
                        </div>
                        <div className="card" style={{ padding: '20px', border: '1px solid #e2e8f0', textAlign: 'center' }}>
                            <div style={{ fontSize: '12px', color: '#64748b', textTransform: 'uppercase', marginBottom: '10px' }}>Risk Profile</div>
                            <div style={{ fontSize: '36px', fontWeight: 'bold', color: riskColor }}>{risk_level}</div>
                            <p style={{ fontSize: '14px', margin: '10px 0 0 0' }}>Assessed risk based on current liabilities.</p>
                        </div>
                    </div>
                </div>

                <div style={{ marginBottom: '30px', breakAfter: 'page' }}>
                    <h2 style={{ fontSize: '18px', borderBottom: '1px solid #e2e8f0', paddingBottom: '8px', marginBottom: '15px' }}>AI-Generated Insights</h2>
                    <div style={{ backgroundColor: '#f8fafc', padding: '15px', borderRadius: '8px', marginBottom: '30px' }}>
                        <ul style={{ paddingLeft: '20px', margin: 0 }}>
                            {insights.map((insight, idx) => (
                                <li key={idx} style={{ marginBottom: '10px', lineHeight: '1.6' }}>{insight}</li>
                            ))}
                        </ul>
                    </div>

                    <h2 style={{ fontSize: '18px', borderBottom: '1px solid #e2e8f0', paddingBottom: '8px', marginBottom: '15px' }}>Strategic Recommendations</h2>
                    <div style={{ backgroundColor: '#f0fdf4', padding: '15px', borderRadius: '8px', border: '1px solid #dcfce7' }}>
                        <ul style={{ paddingLeft: '20px', margin: 0 }}>
                            {recommendations.map((rec, idx) => (
                                <li key={idx} style={{ marginBottom: '10px', lineHeight: '1.6' }}>{rec}</li>
                            ))}
                        </ul>
                    </div>
                </div>

                <div style={{ marginBottom: '30px', breakAfter: 'page' }}>
                    <h2 style={{ fontSize: '18px', borderBottom: '1px solid #e2e8f0', paddingBottom: '8px', marginBottom: '15px' }}>Key Financial Metrics</h2>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px' }}>
                        {Object.entries(metrics).map(([category, values]) => (
                            <div key={category}>
                                <h3 style={{ fontSize: '14px', color: '#64748b', textTransform: 'uppercase', marginBottom: '10px' }}>{category.replace('_', ' ')}</h3>
                                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                    <tbody>
                                        {Object.entries(values).map(([key, value]) => (
                                            <tr key={key} style={{ borderBottom: '1px solid #f1f5f9' }}>
                                                <td style={{ padding: '8px 0', fontSize: '13px', color: '#334155' }}>{key.replace(/_/g, ' ').toUpperCase()}</td>
                                                <td style={{ padding: '8px 0', fontSize: '13px', fontWeight: 'bold', textAlign: 'right' }}>{typeof value === 'number' ? value.toFixed(2) : value}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        ))}
                    </div>
                </div>

                {cash_flow_forecast && (
                    <div style={{ marginBottom: '30px', breakAfter: 'page' }}>
                        <h2 style={{ fontSize: '18px', borderBottom: '1px solid #e2e8f0', paddingBottom: '8px', marginBottom: '15px' }}>12-Month Cash Flow Forecast</h2>
                        <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '20px' }}>
                            <thead>
                                <tr style={{ backgroundColor: '#f8fafc', borderBottom: '1px solid #e2e8f0' }}>
                                    <th style={{ padding: '10px', textAlign: 'left', fontSize: '12px' }}>Month</th>
                                    <th style={{ padding: '10px', textAlign: 'right', fontSize: '12px' }}>Revenue</th>
                                    <th style={{ padding: '10px', textAlign: 'right', fontSize: '12px' }}>Net Income</th>
                                    <th style={{ padding: '10px', textAlign: 'right', fontSize: '12px' }}>Cash Flow</th>
                                </tr>
                            </thead>
                            <tbody>
                                {cash_flow_forecast.monthly_projections.map((row, idx) => (
                                    <tr key={idx} style={{ borderBottom: '1px solid #f1f5f9' }}>
                                        <td style={{ padding: '8px', fontSize: '12px' }}>{row.month}</td>
                                        <td style={{ padding: '8px', textAlign: 'right', fontSize: '12px' }}>₹{row.revenue?.toLocaleString() ?? '0'}</td>
                                        <td style={{ padding: '8px', textAlign: 'right', fontSize: '12px' }}>₹{row.net_income?.toLocaleString() ?? '0'}</td>
                                        <td style={{ padding: '8px', textAlign: 'right', fontSize: '12px' }}>₹{row.net_cash_flow?.toLocaleString() ?? '0'}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        <h3 style={{ fontSize: '14px', marginBottom: '10px' }}>Working Capital Recommendations</h3>
                        <ul style={{ paddingLeft: '20px', fontSize: '13px' }}>
                            {cash_flow_forecast.working_capital_recommendations.map((rec, idx) => (
                                <li key={idx} style={{ marginBottom: '8px' }}>{rec}</li>
                            ))}
                        </ul>
                    </div>
                )}

                {benchmark_comparison && (
                    <div style={{ marginBottom: '30px', breakAfter: 'page' }}>
                        <h2 style={{ fontSize: '18px', borderBottom: '1px solid #e2e8f0', paddingBottom: '8px', marginBottom: '15px' }}>Industry Benchmarking</h2>
                        <div style={{ textAlign: 'center', marginBottom: '20px', padding: '20px', background: '#f8fafc', borderRadius: '8px' }}>
                            <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#38bdf8' }}>{benchmark_comparison.percentile_rank}th Percentile</div>
                            <p style={{ margin: '5px 0' }}>{benchmark_comparison.overall_performance}</p>
                        </div>
                        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                            <thead>
                                <tr style={{ borderBottom: '1px solid #e2e8f0' }}>
                                    <th style={{ padding: '10px', textAlign: 'left' }}>Metric</th>
                                    <th style={{ padding: '10px', textAlign: 'right' }}>Your Value</th>
                                    <th style={{ padding: '10px', textAlign: 'right' }}>Industry Average</th>
                                    <th style={{ padding: '10px', textAlign: 'right' }}>Percentile</th>
                                </tr>
                            </thead>
                            <tbody>
                                {Object.entries(benchmark_comparison.metrics_comparison).map(([key, data]) => (
                                    <tr key={key} style={{ borderBottom: '1px solid #f1f5f9' }}>
                                        <td style={{ padding: '10px', fontSize: '13px' }}>{key.replace(/_/g, ' ').toUpperCase()}</td>
                                        <td style={{ padding: '10px', textAlign: 'right', fontSize: '13px' }}>{typeof data.value === 'number' ? data.value.toFixed(2) : 'N/A'}</td>
                                        <td style={{ padding: '10px', textAlign: 'right', fontSize: '13px' }}>{typeof data.industry_average === 'number' ? data.industry_average.toFixed(2) : 'N/A'}</td>
                                        <td style={{ padding: '10px', textAlign: 'right', fontSize: '13px', fontWeight: 'bold' }}>{data.percentile}th</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                {tax_compliance && (
                    <div style={{ marginBottom: '30px' }}>
                        <h2 style={{ fontSize: '18px', borderBottom: '1px solid #e2e8f0', paddingBottom: '8px', marginBottom: '15px' }}>Tax & Compliance Overview</h2>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                            <div style={{ padding: '15px', border: '1px solid #e2e8f0', borderRadius: '8px' }}>
                                <strong>GST Compliance:</strong> {tax_compliance.gst_status.compliance_status}<br />
                                <span style={{ fontSize: '12px', color: '#64748b' }}>Frequency: {tax_compliance.gst_status.filing_frequency}</span>
                            </div>
                            <div style={{ padding: '15px', border: '1px solid #e2e8f0', borderRadius: '8px' }}>
                                <strong>Income Tax Est:</strong> ₹{tax_compliance.income_tax_estimate?.estimated_tax_liability?.toLocaleString() ?? '0'}<br />
                                <span style={{ fontSize: '12px', color: '#64748b' }}>Taxable Income: ₹{tax_compliance.income_tax_estimate?.taxable_income?.toLocaleString() ?? '0'}</span>
                            </div>
                        </div>
                    </div>
                )}

                <div style={{ marginTop: '50px', borderTop: '1px solid #eee', paddingTop: '20px', textAlign: 'center', fontSize: '11px', color: '#94a3b8' }}>
                    <p>This report is generated automatically based on provided financial data. Please consult with a professional financial advisor for specific business decisions.</p>
                    <p style={{ marginTop: '5px' }}>© 2026 FinHealth AI Platform • Secure Data Analysis</p>
                </div>
            </div>
        </>
    );
};

export default EnhancedDashboard;
