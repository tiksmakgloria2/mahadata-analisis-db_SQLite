import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# KONEKSI DATABASE
# =====================================================

db_file = "penjualan_online_dummy.db"
conn = sqlite3.connect(db_file)

print("=" * 50)
print("ANALISIS DATABASE PENJUALAN ONLINE")
print("=" * 50)

# =====================================================
# TOP 10 PRODUK PENDAPATAN TERTINGGI
# =====================================================

query = """
SELECT
    p.nama_produk,
    SUM(od.subtotal) AS total_pendapatan
FROM order_details od
JOIN products p
ON od.id_produk = p.id_produk
GROUP BY p.id_produk
ORDER BY total_pendapatan DESC
LIMIT 10
"""

top_pendapatan = pd.read_sql(query, conn)

print("\nTOP 10 PRODUK BERDASARKAN PENDAPATAN")
print("-" * 50)
print(top_pendapatan)

# =====================================================
# VISUALISASI MATPLOTLIB
# =====================================================

plt.figure(figsize=(12, 6))

plt.bar(
    top_pendapatan["nama_produk"],
    top_pendapatan["total_pendapatan"],
    color="skyblue"
)

plt.title("Top 10 Produk Berdasarkan Pendapatan", fontsize=14)
plt.xlabel("Nama Produk")
plt.ylabel("Total Pendapatan (Rp)")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Menampilkan nilai di atas batang
for i, nilai in enumerate(top_pendapatan["total_pendapatan"]):
    plt.text(
        i,
        nilai,
        f"{nilai:,.0f}",
        ha="center",
        va="bottom",
        fontsize=8
    )

plt.tight_layout()
plt.show()

conn.close()