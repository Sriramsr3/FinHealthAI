import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Building2, MapPin, Calendar, Briefcase, ChevronRight } from 'lucide-react';
import { useTranslation } from '../context/TranslationContext';

const BusinessProfileForm = ({ onSubmit, onSkip }) => {
    const { t } = useTranslation();
    const [profile, setProfile] = useState({
        name: '',
        business_type: 'private_limited',
        industry: 'services',
        size: 'Medium',
        location: '',
        years_in_operation: ''
    });

    const businessTypes = [
        { value: 'sole_proprietorship', label: t('businessProfile.businessTypes.sole_proprietorship') },
        { value: 'partnership', label: t('businessProfile.businessTypes.partnership') },
        { value: 'private_limited', label: t('businessProfile.businessTypes.private_limited') },
        { value: 'public_limited', label: t('businessProfile.businessTypes.public_limited') },
        { value: 'llp', label: t('businessProfile.businessTypes.llp') }
    ];

    const industries = [
        { value: 'manufacturing', label: t('businessProfile.industries.manufacturing') },
        { value: 'retail', label: t('businessProfile.industries.retail') },
        { value: 'agriculture', label: t('businessProfile.industries.agriculture') },
        { value: 'services', label: t('businessProfile.industries.services') },
        { value: 'logistics', label: t('businessProfile.industries.logistics') },
        { value: 'ecommerce', label: t('businessProfile.industries.ecommerce') },
        { value: 'technology', label: t('businessProfile.industries.technology') },
        { value: 'healthcare', label: t('businessProfile.industries.healthcare') },
        { value: 'hospitality', label: t('businessProfile.industries.hospitality') },
        { value: 'construction', label: t('businessProfile.industries.construction') }
    ];

    const sizes = ['Small', 'Medium', 'Large'];

    const handleChange = (e) => {
        setProfile({
            ...profile,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(profile);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card"
            style={{ maxWidth: '800px', margin: '0 auto' }}
        >
            <div style={{ textAlign: 'center', marginBottom: '32px' }}>
                <Building2 size={48} color="var(--accent-color)" style={{ margin: '0 auto 16px' }} />
                <h2 style={{ marginBottom: '8px' }}>{t('businessProfile.title')}</h2>
                <p style={{ color: 'var(--text-secondary)' }}>
                    {t('businessProfile.subtitle')}
                </p>
            </div>

            <form onSubmit={handleSubmit}>
                <div className="grid grid-2">
                    {/* Business Name */}
                    <div className="input-group" style={{ gridColumn: '1 / -1' }}>
                        <label className="input-label" htmlFor="name">
                            <Building2 size={16} style={{ display: 'inline', marginRight: '8px', verticalAlign: '-2px' }} />
                            {t('businessProfile.businessName')} {t('businessProfile.required')}
                        </label>
                        <input
                            type="text"
                            id="name"
                            name="name"
                            value={profile.name}
                            onChange={handleChange}
                            className="form-input"
                            required
                            placeholder={t('businessProfile.businessNamePlaceholder')}
                        />
                    </div>

                    {/* Business Type */}
                    <div className="input-group">
                        <label className="input-label" htmlFor="business_type">
                            <Briefcase size={16} style={{ display: 'inline', marginRight: '8px', verticalAlign: '-2px' }} />
                            {t('businessProfile.businessType')} {t('businessProfile.required')}
                        </label>
                        <select
                            id="business_type"
                            name="business_type"
                            value={profile.business_type}
                            onChange={handleChange}
                            className="form-input"
                            required
                        >
                            {businessTypes.map(type => (
                                <option key={type.value} value={type.value}>{type.label}</option>
                            ))}
                        </select>
                    </div>

                    {/* Industry */}
                    <div className="input-group">
                        <label className="input-label" htmlFor="industry">
                            {t('businessProfile.industry')} {t('businessProfile.required')}
                        </label>
                        <select
                            id="industry"
                            name="industry"
                            value={profile.industry}
                            onChange={handleChange}
                            className="form-input"
                            required
                        >
                            {industries.map(ind => (
                                <option key={ind.value} value={ind.value}>{ind.label}</option>
                            ))}
                        </select>
                    </div>

                    {/* Business Size */}
                    <div className="input-group">
                        <label className="input-label" htmlFor="size">
                            {t('businessProfile.businessSize')}
                        </label>
                        <select
                            id="size"
                            name="size"
                            value={profile.size}
                            onChange={handleChange}
                            className="form-input"
                        >
                            {sizes.map(size => (
                                <option key={size} value={size}>{t(`businessProfile.sizes.${size}`)}</option>
                            ))}
                        </select>
                    </div>

                    {/* Years in Operation */}
                    <div className="input-group">
                        <label className="input-label" htmlFor="years_in_operation">
                            <Calendar size={16} style={{ display: 'inline', marginRight: '8px', verticalAlign: '-2px' }} />
                            {t('businessProfile.yearsInOperation')}
                        </label>
                        <input
                            type="number"
                            id="years_in_operation"
                            name="years_in_operation"
                            value={profile.years_in_operation}
                            onChange={handleChange}
                            className="form-input"
                            min="0"
                            placeholder={t('businessProfile.yearsPlaceholder')}
                        />
                    </div>

                    {/* Location */}
                    <div className="input-group" style={{ gridColumn: '1 / -1' }}>
                        <label className="input-label" htmlFor="location">
                            <MapPin size={16} style={{ display: 'inline', marginRight: '8px', verticalAlign: '-2px' }} />
                            {t('businessProfile.location')}
                        </label>
                        <input
                            type="text"
                            id="location"
                            name="location"
                            value={profile.location}
                            onChange={handleChange}
                            className="form-input"
                            placeholder={t('businessProfile.locationPlaceholder')}
                        />
                    </div>
                </div>

                <div style={{ display: 'flex', gap: '16px', marginTop: '32px', justifyContent: 'flex-end' }}>
                    {onSkip && (
                        <button
                            type="button"
                            className="btn"
                            onClick={onSkip}
                            style={{ background: 'transparent', color: 'var(--text-secondary)' }}
                        >
                            {t('businessProfile.skipButton')}
                        </button>
                    )}
                    <button type="submit" className="btn btn-primary">
                        {t('businessProfile.continueButton')}
                        <ChevronRight size={18} style={{ marginLeft: '8px', verticalAlign: '-3px' }} />
                    </button>
                </div>
            </form>
        </motion.div>
    );
};

export default BusinessProfileForm;
