import React from 'react';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart, Pie } from 'recharts';
import { AlertTriangle, CheckCircle, TrendingUp, DollarSign } from 'lucide-react';

const Dashboard = ({ data }) => {
    if (!data) return null;

    const { score, risk_level, insights, recommendations, metrics } = data;

    const scoreColor = score >= 80 ? '#22c55e' : score >= 50 ? '#eab308' : '#ef4444';

    const metricData = [
        { name: 'Current Ratio', value: metrics.current_ratio },
        { name: 'Profit Margin', value: metrics.net_profit_margin },
        { name: 'Debt/Equity', value: metrics.debt_to_equity },
    ];

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}
        >
            {/* Header Cards */}
            <div className="grid grid-2">
                <motion.div
                    className="card metric-card"
                    whileHover={{ scale: 1.02 }}
                >
                    <div className="metric-label">Financial Health Score</div>
                    <div className="metric-value" style={{ color: scoreColor }}>{score}/100</div>
                    <div style={{ color: scoreColor, fontWeight: 500 }}>{risk_level} Risk</div>
                </motion.div>

                <motion.div
                    className="card"
                    whileHover={{ scale: 1.02 }}
                >
                    <h3>Key Metrics Visualization</h3>
                    <div style={{ width: '100%', height: 150 }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={metricData} layout="vertical">
                                <XAxis type="number" hide />
                                <YAxis dataKey="name" type="category" width={100} tick={{ fill: '#94a3b8' }} />
                                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none' }} />
                                <Bar dataKey="value" fill="#38bdf8" radius={[0, 4, 4, 0]}>
                                    {metricData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={index === 0 ? '#38bdf8' : index === 1 ? '#22c55e' : '#f472b6'} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>
            </div>

            {/* Insights Section */}
            <div className="grid grid-2">
                <div className="card">
                    <h3><TrendingUp size={20} style={{ marginRight: 8, verticalAlign: 'middle' }} /> AI Insights</h3>
                    <ul style={{ paddingLeft: 20, marginTop: 16 }}>
                        {insights.map((insight, idx) => (
                            <li key={idx} style={{ marginBottom: 12, lineHeight: 1.5 }}>
                                {insight}
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="card">
                    <h3><CheckCircle size={20} style={{ marginRight: 8, verticalAlign: 'middle' }} /> Strategic Recommendations</h3>
                    <ul style={{ paddingLeft: 20, marginTop: 16 }}>
                        {recommendations.map((rec, idx) => (
                            <li key={idx} style={{ marginBottom: 12, lineHeight: 1.5 }}>
                                {rec}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </motion.div>
    );
};

export default Dashboard;
