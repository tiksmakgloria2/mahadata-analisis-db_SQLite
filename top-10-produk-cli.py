import sqlite3
import pandas as pd

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
conn.close()