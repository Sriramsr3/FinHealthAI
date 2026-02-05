import pandas as pd
import pdfplumber
import io
from typing import Dict, Any, Optional
from fastapi import UploadFile, HTTPException
import logging

logger = logging.getLogger(__name__)

class DocumentParser:
    """Multi-format document parser for financial statements"""
    
    @staticmethod
    async def parse_file(file: UploadFile) -> Dict[str, Any]:
        """
        Parse uploaded financial document
        
        Args:
            file: Uploaded file (CSV, XLSX, or PDF)
            
        Returns:
            Dictionary with parsed financial data
        """
        filename = file.filename.lower()
        
        try:
            content = await file.read()
            
            if filename.endswith('.csv'):
                return DocumentParser._parse_csv(content)
            elif filename.endswith(('.xlsx', '.xls')):
                return DocumentParser._parse_excel(content)
            elif filename.endswith('.pdf'):
                return DocumentParser._parse_pdf(content)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported file format. Please upload CSV, XLSX, or PDF"
                )
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error parsing file {filename}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")
    
    @staticmethod
    def _parse_csv(content: bytes) -> Dict[str, Any]:
        """Parse CSV file"""
        try:
            df = pd.read_csv(io.BytesIO(content))
            return DocumentParser._extract_financial_data(df)
        except Exception as e:
            raise Exception(f"CSV parsing error: {str(e)}")
    
    @staticmethod
    def _parse_excel(content: bytes) -> Dict[str, Any]:
        """Parse Excel file"""
        try:
            df = pd.read_excel(io.BytesIO(content))
            return DocumentParser._extract_financial_data(df)
        except Exception as e:
            raise Exception(f"Excel parsing error: {str(e)}")
    
    @staticmethod
    def _parse_pdf(content: bytes) -> Dict[str, Any]:
        """Parse PDF file (extract tables)"""
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                # Extract tables from all pages
                all_tables = []
                for page in pdf.pages:
                    tables = page.extract_tables()
                    if tables:
                        all_tables.extend(tables)
                
                if not all_tables:
                    raise Exception("No tables found in PDF")
                
                # Convert first table to DataFrame
                df = pd.DataFrame(all_tables[0][1:], columns=all_tables[0][0])
                return DocumentParser._extract_financial_data(df)
                
        except Exception as e:
            raise Exception(f"PDF parsing error: {str(e)}")
    
    @staticmethod
    def _extract_financial_data(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Extract financial data from DataFrame using intelligent column mapping
        
        Args:
            df: Pandas DataFrame with financial data
            
        Returns:
            Dictionary with standardized financial metrics
        """

        
        # Column mapping dictionary
        column_mappings = {
            'revenue': ['revenue', 'total_revenue', 'sales', 'total_sales', 'income', 'turnover'],
            'cogs': ['cogs', 'cost_of_goods_sold', 'cost_of_sales', 'direct_costs'],
            'operating_expenses': ['operating_expenses', 'opex', 'operating_costs', 'expenses'],
            'net_income': ['net_income', 'net_profit', 'profit', 'earnings', 'net_earnings'],
            'total_assets': ['total_assets', 'assets'],
            'current_assets': ['current_assets', 'liquid_assets'],
            'total_liabilities': ['total_liabilities', 'liabilities'],
            'current_liabilities': ['current_liabilities', 'short_term_liabilities'],
            'inventory': ['inventory', 'stock'],
            'receivables': ['receivables', 'accounts_receivable', 'debtors'],
            'payables': ['payables', 'accounts_payable', 'creditors'],
            'cash': ['cash', 'cash_and_equivalents', 'cash_balance']
        }

        # Normalize column names in the original dataframe first
        df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')

        # Check for Transpose Scenario (Long Format: Metric in rows, Value in columns)
        # Heuristic: If typical headers are NOT in columns, but ARE in the first column 
        all_keywords = [kw for key in column_mappings for kw in column_mappings[key]]
        has_wide_keywords = any(kw in df.columns for kw in all_keywords)
        
        if not has_wide_keywords and df.shape[1] >= 2:
            try:
                # Check first column for keywords
                first_col_values = df.iloc[:, 0].astype(str).str.lower().str.strip().str.replace(' ', '_')
                matches = first_col_values.isin(all_keywords).sum()
                
                if matches > 0:
                    logger.info("Detected Long format (Key-Value rows). Transposing dataframe.")
                    # Prepare for transpose: Take first two columns, normalize key column
                    temp_df = df.iloc[:, :2].copy()
                    temp_df.columns = ['key', 'value']
                    temp_df['key'] = temp_df['key'].astype(str).str.lower().str.strip().str.replace(' ', '_')
                    
                    # Convert to wide format
                    # Drop duplicates to avoid index errors
                    temp_df = temp_df.drop_duplicates(subset='key')
                    
                    # Set index and transpose
                    df_transposed = temp_df.set_index('key').T
                    df_transposed.reset_index(drop=True, inplace=True)
                    df = df_transposed
            except Exception as e:
                logger.warning(f"Attempt to transpose failed: {str(e)}")
        
        def find_value(field_name: str, mappings: list) -> float:
            """Find value from DataFrame using column mappings"""
            for col_name in mappings:
                if col_name in df.columns:
                    try:
                        value = df[col_name].iloc[0] if len(df) > 0 else 0
                        # Handle string values with currency symbols
                        if isinstance(value, str):
                            value = value.replace(',', '').replace('$', '').replace('₹', '').strip()
                        return float(value)
                    except (ValueError, TypeError, IndexError):
                        continue
            return 0.0
        
        # Extract all financial metrics
        financial_data = {
            field: find_value(field, mappings)
            for field, mappings in column_mappings.items()
        }
        
        # Validation
        if financial_data['revenue'] == 0 and financial_data['total_assets'] == 0:
            raise Exception(
                "Could not extract financial data. Please ensure your file contains "
                "columns like 'Revenue', 'Total Assets', 'Net Income', etc."
            )
        
        return financial_data

document_parser = DocumentParser()
