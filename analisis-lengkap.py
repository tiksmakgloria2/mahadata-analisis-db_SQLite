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
# JUMLAH DATA SETIAP TABEL
# =====================================================

tables = [
    "users",
    "products",
    "categories",
    "orders",
    "order_details",
    "payments",
    "reviews"
]

print("\nJUMLAH RECORD PER TABEL")
print("-" * 50)

for table in tables:
    query = f"SELECT COUNT(*) AS total FROM {table}"
    total = pd.read_sql(query, conn).iloc[0, 0]
    print(f"{table:15} : {total}")

# =====================================================
# TOTAL OMZET
# =====================================================

query = """
SELECT
    SUM(jumlah_bayar) AS total_omzet
FROM payments
"""

omzet = pd.read_sql(query, conn)

print("\nTOTAL OMZET")
print("-" * 50)
print(f"Rp {omzet['total_omzet'][0]:,.0f}")

# =====================================================
# TOP 10 PRODUK TERLARIS
# =====================================================

query = """
SELECT
    p.nama_produk,
    SUM(od.jumlah) AS total_terjual
FROM order_details od
JOIN products p
ON od.id_produk = p.id_produk
GROUP BY p.id_produk
ORDER BY total_terjual DESC
LIMIT 10
"""

top_produk = pd.read_sql(query, conn)

print("\nTOP 10 PRODUK TERLARIS")
print("-" * 50)
print(top_produk)

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
# DISTRIBUSI RATING
# =====================================================

query = """
SELECT
    rating,
    COUNT(*) AS jumlah
FROM reviews
GROUP BY rating
ORDER BY rating
"""

rating_df = pd.read_sql(query, conn)

print("\nDISTRIBUSI RATING")
print("-" * 50)
print(rating_df)

# =====================================================
# PENJUALAN PER BULAN
# =====================================================

query = """
SELECT
    substr(tanggal_pesanan, 1, 7) AS bulan,
    SUM(total_harga) AS total
FROM orders
GROUP BY bulan
ORDER BY bulan
"""

penjualan_bulanan = pd.read_sql(query, conn)

print("\nPENJUALAN PER BULAN")
print("-" * 50)
print(penjualan_bulanan)

# =====================================================
# TOP 10 CUSTOMER
# =====================================================

query = """
SELECT
    u.nama,
    COUNT(o.id_pesanan) AS total_order,
    SUM(o.total_harga) AS total_belanja
FROM users u
JOIN orders o
ON u.id_user = o.id_user
GROUP BY u.id_user
ORDER BY total_belanja DESC
LIMIT 10
"""

top_customer = pd.read_sql(query, conn)

print("\nTOP 10 CUSTOMER")
print("-" * 50)
print(top_customer)

# =====================================================
# VISUALISASI
# =====================================================

plt.figure(figsize=(10, 5))

plt.bar(
    top_produk["nama_produk"],
    top_produk["total_terjual"]
)

plt.title("Top 10 Produk Terlaris")
plt.xlabel("Produk")
plt.ylabel("Jumlah Terjual")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# =====================================================

plt.figure(figsize=(8, 5))

plt.pie(
    rating_df["jumlah"],
    labels=rating_df["rating"],
    autopct="%1.1f%%"
)

plt.title("Distribusi Rating")
plt.show()

# =====================================================

plt.figure(figsize=(10, 5))

plt.plot(
    penjualan_bulanan["bulan"],
    penjualan_bulanan["total"],
    marker="o"
)

plt.title("Trend Penjualan Bulanan")
plt.xlabel("Bulan")
plt.ylabel("Omzet")

plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()

# =====================================================
# EXPORT KE EXCEL
# =====================================================

with pd.ExcelWriter("laporan_analisis_penjualan.xlsx") as writer:

    top_produk.to_excel(
        writer,
        sheet_name="Top Produk",
        index=False
    )

    top_pendapatan.to_excel(
        writer,
        sheet_name="Pendapatan Produk",
        index=False
    )

    rating_df.to_excel(
        writer,
        sheet_name="Rating",
        index=False
    )

    penjualan_bulanan.to_excel(
        writer,
        sheet_name="Penjualan Bulanan",
        index=False
    )

    top_customer.to_excel(
        writer,
        sheet_name="Top Customer",
        index=False
    )

print("\nFile laporan_analisis_penjualan.xlsx berhasil dibuat.")

conn.close()