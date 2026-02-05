import React, { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { UploadCloud, FileText, Calculator } from 'lucide-react';
import { useTranslation } from '../context/TranslationContext';

const FinancialForm = ({ onAnalyze, businessProfile, language }) => {
    const { t } = useTranslation();
    const [activeTab, setActiveTab] = useState('manual'); // 'manual' or 'upload'
    const [formData, setFormData] = useState({
        revenue: 1000000,
        cogs: 600000,
        operating_expenses: 200000,
        net_income: 200000,
        total_assets: 800000,
        current_assets: 400000,
        total_liabilities: 300000,
        current_liabilities: 150000,
        inventory: 100000,
        receivables: 150000,
        payables: 80000
    });

    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        const value = e.target.value;
        setFormData({
            ...formData,
            [e.target.name]: value === '' ? '' : parseFloat(value)
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        const cleanedData = Object.fromEntries(
            Object.entries(formData).map(([key, value]) => [key, value === '' ? 0 : value])
        );

        try {
            // Send comprehensive analysis request
            const analysisRequest = {
                business_profile: businessProfile || {
                    name: "My Business",
                    business_type: "private_limited",
                    industry: "services",
                    size: "Medium"
                },
                financial_statement: cleanedData,
                language: language || "en"
            };

            const response = await axios.post('https://finhealthai.onrender.com/analyze', analysisRequest);
            onAnalyze(response.data);
        } catch (error) {
            console.error("Error analyzing data:", error);
            const errorMsg = error.response?.data?.detail || "Failed to connect to analysis engine.";
            alert(`Analysis failed: ${errorMsg}`);
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setLoading(true);
        const uploadData = new FormData();
        uploadData.append('file', file);

        try {
            // Add business profile as query parameters
            const params = new URLSearchParams({
                business_name: businessProfile?.name || 'My Business',
                business_type: businessProfile?.business_type || 'private_limited',
                industry: businessProfile?.industry || 'services',
                language: language || 'en'
            });

            const response = await axios.post(
                `https://finhealthai.onrender.com/upload?${params.toString()}`,
                uploadData,
                { headers: { 'Content-Type': 'multipart/form-data' } }
            );
            onAnalyze(response.data);
        } catch (error) {
            console.error("Upload error:", error);
            const errorMsg = error.response?.data?.detail || "Upload failed";
            alert(`Upload failed: ${errorMsg}`);
        } finally {
            setLoading(false);
        }
    };

    const formFields = [
        { name: 'revenue', label: t('financialForm.revenue') },
        { name: 'cogs', label: t('financialForm.cogs') },
        { name: 'operating_expenses', label: t('financialForm.operatingExpenses') },
        { name: 'net_income', label: t('financialForm.netIncome') },
        { name: 'total_assets', label: t('financialForm.totalAssets') },
        { name: 'current_assets', label: t('financialForm.currentAssets') },
        { name: 'total_liabilities', label: t('financialForm.totalLiabilities') },
        { name: 'current_liabilities', label: t('financialForm.currentLiabilities') },
        { name: 'inventory', label: t('financialForm.inventory') },
        { name: 'receivables', label: t('financialForm.receivables') },
        { name: 'payables', label: t('financialForm.payables') },
    ];

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card"
        >
            <div style={{ display: 'flex', gap: '20px', marginBottom: '24px', borderBottom: '1px solid var(--glass-border)', paddingBottom: '16px' }}>
                <button
                    className={`btn ${activeTab === 'manual' ? 'btn-primary' : ''}`}
                    style={{ background: activeTab === 'manual' ? undefined : 'transparent', color: activeTab === 'manual' ? '#fff' : 'var(--text-secondary)' }}
                    onClick={() => setActiveTab('manual')}
                >
                    <Calculator size={18} style={{ marginRight: 8, verticalAlign: '-3px' }} />
                    {t('financialForm.manualEntry')}
                </button>
                <button
                    className={`btn ${activeTab === 'upload' ? 'btn-primary' : ''}`}
                    style={{ background: activeTab === 'upload' ? undefined : 'transparent', color: activeTab === 'upload' ? '#fff' : 'var(--text-secondary)' }}
                    onClick={() => setActiveTab('upload')}
                >
                    <UploadCloud size={18} style={{ marginRight: 8, verticalAlign: '-3px' }} />
                    {t('financialForm.uploadDocuments')}
                </button>
            </div>

            {activeTab === 'manual' ? (
                <form onSubmit={handleSubmit}>
                    <div className="grid grid-2">
                        {formFields.map((field) => (
                            <div key={field.name} className="input-group">
                                <label className="input-label" htmlFor={field.name}>{field.label}</label>
                                <input
                                    type="number"
                                    id={field.name}
                                    name={field.name}
                                    value={formData[field.name]}
                                    onChange={handleChange}
                                    className="form-input"
                                    min={field.name === 'net_income' ? undefined : "0"}
                                    step="any"
                                />
                                {field.name === 'net_income' && (
                                    <small style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
                                        {t('financialForm.netIncomeNote')}
                                    </small>
                                )}
                            </div>
                        ))}
                    </div>
                    <div style={{ marginTop: '20px', textAlign: 'right' }}>
                        <button type="submit" className="btn btn-primary" disabled={loading}>
                            {loading ? t('financialForm.analyzingButton') : t('financialForm.analyzeButton')}
                        </button>
                    </div>
                </form>
            ) : (
                <div style={{ textAlign: 'center', padding: '40px 20px', border: '2px dashed var(--bg-card)', borderRadius: '12px' }}>
                    <UploadCloud size={48} color="var(--accent-color)" />
                    <h3 style={{ marginTop: '16px' }}>{t('financialForm.uploadTitle')}</h3>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
                        {t('financialForm.uploadSubtitle')}
                    </p>

                    <input
                        type="file"
                        id="file-upload"
                        style={{ display: 'none' }}
                        accept=".csv, .xlsx, .xls"
                        onChange={handleFileUpload}
                    />
                    <label htmlFor="file-upload" className="btn btn-primary">
                        {loading ? t('financialForm.processingFile') : t('financialForm.selectDocument')}
                    </label>

                    <div style={{ marginTop: '30px', textAlign: 'left', background: 'var(--bg-primary)', padding: '16px', borderRadius: '8px' }}>
                        <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '12px' }}>
                            <FileText size={16} color="var(--accent-color)" />
                            <span style={{ fontWeight: 600 }}>{t('financialForm.templateHeader')}</span>
                        </div>
                        <code style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'block', wordBreak: 'break-all' }}>
                            {t('financialForm.templateText')}
                        </code>
                    </div>
                </div>
            )}
        </motion.div>
    );
};

export default FinancialForm;
