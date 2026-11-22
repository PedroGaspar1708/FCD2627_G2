import functools
import os
import io
import pandas as pd
import requests

CICLO = "2021"      # ano inicial do ciclo
SUFIXO = "L"        # _L = 2021-2023
BASE = f"https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{CICLO}/DataFiles/"
RAW_PATH = os.path.join("data", "raw")
os.makedirs(RAW_PATH, exist_ok=True)


def corrigir_zeros(df: pd.DataFrame) -> pd.DataFrame:
    """Nos .xpt do NHANES, alguns zeros vêm codificados como ~5.397605e-79; converte-os para 0."""
    num = df.select_dtypes("number").columns
    df[num] = df[num].mask(df[num].abs() < 1e-50, 0)
    return df


def carregar(nome: str, obrigatorio: bool = True) -> pd.DataFrame:
    """Descarrega e lê um ficheiro .xpt do NHANES diretamente em memória (nada é guardado em disco)."""
    fich = f"{nome}_{SUFIXO}.xpt"
    try:
        r = requests.get(BASE + fich, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
        r.raise_for_status()
    except requests.RequestException as e:
        if obrigatorio:
            raise
        print(f"[aviso] {fich} não disponível ({e}); ignorado.")
        return None
    df = pd.read_sas(io.BytesIO(r.content), format="xport")
    return corrigir_zeros(df)

def sel(df: pd.DataFrame, colunas: list) -> pd.DataFrame:
    """Mantém SEQN + as colunas pedidas que existam no DataFrame."""
    if df is None:
        return None
    em_falta = [c for c in colunas if c not in df.columns]
    if em_falta:
        print(f"[aviso] colunas ausentes: {em_falta}")
    return df[["SEQN"] + [c for c in colunas if c in df.columns]]


def exportar_como_tabela_excel(df: pd.DataFrame, nome_ficheiro: str, nome_folha: str = "Dados") -> None:
    """Exporta um DataFrame formatado como uma Tabela Excel interativa."""
    caminho_completo = os.path.join(RAW_PATH, nome_ficheiro)
    
    with pd.ExcelWriter(caminho_completo, engine="xlsxwriter") as writer:
        df.to_excel(
            writer, sheet_name=nome_folha, startrow=1, header=False, index=False, na_rep="NA"
        )
        workbook = writer.book
        worksheet = writer.sheets[nome_folha]
        (max_row, max_col) = df.shape

        column_settings = [{"header": column} for column in df.columns]

        worksheet.add_table(
            0,
            0,
            max_row,
            max_col - 1,
            {
                "columns": column_settings,
                "style": "Table Style Medium 9",
                "name": "TabelaNHANES_RAW",
            },
        )

        for i, col in enumerate(df.columns):
            largura_maxima = max(df[col].astype(str).map(len).max(), len(str(col))) + 3
            largura_maxima = min(largura_maxima, 50)
            worksheet.set_column(i, i, largura_maxima)

    print(f"Ficheiro '{caminho_completo}' gerado com sucesso!")


def main():
    print("A iniciar a extração de dados 100% RAW do NHANES...")

    # --- 1. Seleção das Colunas por Módulo ---
    NUTRIENTES = ["CAFF", "SUGR", "FIBE", "CARB", "KCAL", "MFAT", "PFAT", "SFAT", "SODI",
                  "POTA", "VC", "ATOC", "PROT", "VB12", "CALC", "VB6"]

    dr1 = sel(carregar("DR1TOT"), [f"DR1T{n}" for n in NUTRIENTES])
    dr2 = sel(carregar("DR2TOT"), [f"DR2T{n}" for n in NUTRIENTES])
    demo = sel(carregar("DEMO"), ["DMDEDUC2", "RIAGENDR", "RIDAGEYR", "INDFMPIR"])
    
    bmx = sel(carregar("BMX"), ["BMXBMI"])
    hiq = sel(carregar("HIQ"), ["HIQ011"])
    paq = sel(carregar("PAQ"), ["PAD680", "PAD790Q", "PAD790U"])
    bpq = sel(carregar("BPQ"), ["BPQ030"])
    alq = sel(carregar("ALQ"), ["ALQ121"])
    smq = sel(carregar("SMQ"), ["SMQ040", "SMQ020"])
    slq = sel(carregar("SLQ"), ["SLD012", "SLD013"])
    ocq = sel(carregar("OCQ"), ["OCQ180"])
        
    bio = sel(carregar("BIOPRO"), ["LBXSAL", "LBXSCR", "LBXSGL", "LBXSAPSI"])
    crp = sel(carregar("HSCRP"), ["LBXHSCRP"])
    cbc = sel(carregar("CBC"), ["LBXLYPCT", "LBXMCVSI", "LBXRDW", "LBXWBCSI"])
    tchol = sel(carregar("TCHOL"), ["LBDTCSI"])

    # Lista de todos os dataframes carregados sem qualquer filtro/limpeza
    dfs = [demo, dr1, dr2, bmx, bpq, hiq, paq, alq, smq, slq, ocq, bio, crp, cbc, tchol]
    dfs_validos = [d for d in dfs if d is not None]

    # --- 2. Junção Externa Completa (FULL OUTER JOIN) ---
    df_raw_merged = functools.reduce(
        lambda left, right: pd.merge(left, right, on="SEQN", how="outer"),
        dfs_validos
    )

    df_raw_merged["CICLO"] = "2021-2023"

    print(f"Total de registos únicos (SEQN) extraídos: {len(df_raw_merged)}")
    print(f"Total de colunas extraídas: {len(df_raw_merged.columns)}")

    # --- 3. Exportação para Excel na pasta data/raw ---
    exportar_como_tabela_excel(df_raw_merged, "nhanes_raw_merged_2021_2023.xlsx", nome_folha="NHANES_RAW")


if __name__ == "__main__":
    main()