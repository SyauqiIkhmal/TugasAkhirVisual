-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 22, 2026 at 01:14 PM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `photo_studio_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `fotografer`
--

CREATE TABLE `fotografer` (
  `id_fotografer` int NOT NULL,
  `nama` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `spesialisasi` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nomor_hp` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `fotografer`
--

INSERT INTO `fotografer` (`id_fotografer`, `nama`, `spesialisasi`, `nomor_hp`, `created_at`, `updated_at`) VALUES
(1, 'Maya Photographer', 'Wedding', '082134567890', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(2, 'Reza Studio', 'Portrait', '082134567891', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(3, 'Linda Creative', 'Fashion', '082134567892', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(4, 'Anton Photography', 'Corporate', '082134567893', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(5, 'Sari Visual', 'Family', '082134567894', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(6, 'Denny Captures', 'Event', '082134567895', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(7, 'Rina Moments', 'Prewedding', '082134567896', '2025-10-03 08:18:02', '2025-10-03 08:18:02');

-- --------------------------------------------------------

--
-- Table structure for table `jadwal`
--

CREATE TABLE `jadwal` (
  `id_sesi` int NOT NULL,
  `id_klien` int NOT NULL,
  `id_fotografer` int NOT NULL,
  `id_studio` int NOT NULL,
  `tanggal_waktu` datetime NOT NULL,
  `jenis_paket` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` enum('Booked','Selesai','Batal') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Booked',
  `catatan` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `jadwal`
--

INSERT INTO `jadwal` (`id_sesi`, `id_klien`, `id_fotografer`, `id_studio`, `tanggal_waktu`, `jenis_paket`, `status`, `catatan`, `created_at`, `updated_at`) VALUES
(1, 3, 3, 6, '2025-10-02 00:18:03', 'Product', 'Selesai', 'Sesi foto outdoor dengan durasi 3 jam', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(2, 2, 1, 5, '2025-09-19 08:18:03', 'Portrait', 'Batal', 'Sesi foto outdoor dengan durasi 3 jam', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(3, 3, 6, 2, '2025-09-17 08:18:03', 'Prewedding', 'Selesai', 'Sesi foto indoor dengan durasi 2 jam', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(4, 1, 3, 1, '2025-10-02 01:18:03', 'Prewedding', 'Selesai', 'Sesi foto studio dengan durasi 5 jam', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(5, 3, 5, 5, '2025-09-17 04:18:03', 'Fashion', 'Selesai', 'Sesi foto indoor dengan durasi 2 jam', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(6, 1, 1, 3, '2025-09-29 06:18:03', 'Wedding', 'Selesai', 'Sesi foto indoor dengan durasi 3 jam', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(7, 4, 2, 4, '2025-09-10 04:18:03', 'Portrait', 'Selesai', 'Sesi foto indoor dengan durasi 4 jam', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(8, 2, 4, 3, '2025-09-20 07:18:03', 'Portrait', 'Selesai', 'Sesi foto indoor dengan durasi 4 jam', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(9, 4, 2, 3, '2025-09-16 02:18:03', 'Family', 'Batal', 'Sesi foto studio dengan durasi 6 jam', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(10, 3, 3, 1, '2025-09-30 00:18:03', 'Wedding', 'Batal', 'Sesi foto indoor dengan durasi 6 jam', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(11, 1, 3, 4, '2025-09-29 08:18:03', 'Wedding', 'Selesai', 'Sesi foto studio dengan durasi 5 jam', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(12, 1, 2, 5, '2025-09-10 07:18:03', 'Fashion', 'Batal', 'Sesi foto studio dengan durasi 3 jam', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(13, 6, 4, 5, '2025-09-06 22:18:03', 'Corporate', 'Selesai', 'Sesi foto indoor dengan durasi 2 jam', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(14, 6, 2, 4, '2025-09-19 07:18:03', 'Wedding', 'Batal', 'Sesi foto studio dengan durasi 5 jam', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(15, 6, 4, 6, '2025-09-02 23:18:03', 'Prewedding', 'Batal', 'Sesi foto outdoor dengan durasi 4 jam', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(16, 3, 5, 4, '2025-11-10 01:18:03', 'Family', 'Booked', 'Booking untuk ulang tahun', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(17, 5, 2, 5, '2025-11-23 10:18:03', 'Prewedding', 'Booked', 'Booking untuk family gathering', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(18, 5, 7, 2, '2025-11-12 01:18:03', 'Corporate', 'Booked', 'Booking untuk corporate event', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(19, 2, 7, 2, '2025-11-05 09:18:03', 'Event', 'Booked', 'Booking untuk ulang tahun', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(20, 1, 4, 2, '2025-10-22 09:18:03', 'Product', 'Booked', 'Booking untuk wisuda', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(21, 7, 3, 3, '2025-11-02 02:18:03', 'Product', 'Booked', 'Booking untuk pernikahan', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(22, 7, 3, 5, '2025-11-05 07:18:03', 'Wedding', 'Booked', 'Booking untuk pernikahan', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(23, 2, 6, 3, '2025-10-23 05:18:03', 'Birthday', 'Booked', 'Booking untuk wisuda', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(24, 7, 2, 1, '2025-11-03 07:18:03', 'Product', 'Booked', 'Booking untuk wisuda', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(25, 4, 6, 5, '2025-10-31 09:18:03', 'Portrait', 'Booked', 'Booking untuk corporate event', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(26, 3, 5, 4, '2025-11-01 02:18:03', 'Family', 'Booked', 'Booking untuk pernikahan', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(27, 1, 6, 1, '2025-10-06 01:18:03', 'Product', 'Booked', 'Booking untuk ulang tahun', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(28, 8, 7, 4, '2025-11-26 04:18:03', 'Family', 'Batal', 'Booking untuk pernikahan', '2025-10-03 08:18:03', '2025-11-25 14:34:04'),
(29, 1, 4, 3, '2025-10-27 06:18:03', 'Portrait', 'Booked', 'Booking untuk pernikahan', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(30, 6, 7, 3, '2025-10-18 01:18:03', 'Prewedding', 'Booked', 'Booking untuk wisuda', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(31, 1, 3, 2, '2025-10-17 10:18:03', 'Birthday', 'Booked', 'Booking untuk corporate event', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(32, 4, 6, 3, '2025-11-01 04:18:03', 'Birthday', 'Booked', 'Booking untuk ulang tahun', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(33, 4, 5, 5, '2025-10-19 10:18:03', 'Birthday', 'Booked', 'Booking untuk ulang tahun', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(34, 6, 6, 2, '2025-10-07 07:18:03', 'Fashion', 'Booked', 'Booking untuk corporate event', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(35, 6, 2, 1, '2025-11-24 04:18:03', 'Product', 'Booked', 'Booking untuk ulang tahun', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(36, 5, 7, 6, '2025-10-04 04:18:03', 'Graduation', 'Booked', 'Sesi foto mendatang - pastikan semua peralatan siap', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(37, 1, 1, 1, '2025-10-04 07:18:03', 'Product', 'Booked', 'Sesi foto mendatang - pastikan semua peralatan siap', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(38, 2, 3, 4, '2025-10-07 02:18:03', 'Portrait', 'Booked', 'Sesi foto mendatang - pastikan semua peralatan siap', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(39, 1, 5, 4, '2025-10-04 05:18:03', 'Prewedding', 'Booked', 'Sesi foto mendatang - pastikan semua peralatan siap', '2025-10-03 08:18:03', '2025-10-03 08:18:03'),
(40, 7, 7, 4, '2025-10-05 06:18:03', 'Product', 'Booked', 'Sesi foto mendatang - pastikan semua peralatan siap', '2025-10-03 08:18:03', '2025-10-03 08:18:03');

-- --------------------------------------------------------

--
-- Table structure for table `klien`
--

CREATE TABLE `klien` (
  `id_klien` int NOT NULL,
  `nama` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nomor_hp` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `alamat` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `klien`
--

INSERT INTO `klien` (`id_klien`, `nama`, `nomor_hp`, `email`, `alamat`, `created_at`, `updated_at`) VALUES
(1, 'Ahmad Wijaya', '081234567890', 'ahmad.wijaya@email.com', 'Jl. Sudirman No. 123, Jakarta', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(2, 'Siti Nurhaliza', '081234567891', 'siti.nurhaliza@email.com', 'Jl. Thamrin No. 456, Jakarta', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(3, 'Budi Santoso', '081234567892', 'budi.santoso@email.com', 'Jl. Gatot Subroto No. 789, Jakarta', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(4, 'Dewi Lestari', '081234567893', 'dewi.lestari@email.com', 'Jl. Kuningan No. 321, Jakarta', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(5, 'Eko Prasetyo', '081234567894', 'eko.prasetyo@email.com', 'Jl. Kemang No. 654, Jakarta', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(6, 'Fitri Handayani', '081234567895', 'fitri.handayani@email.com', 'Jl. Pondok Indah No. 987, Jakarta', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(7, 'Gunawan Susanto', '081234567896', 'gunawan.susanto@email.com', 'Jl. Senayan No. 147, Jakarta', '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(8, 'Hani Puspita', '081234567897', 'hani.puspita@email.com', 'Jl. Menteng No. 258, Jakarta', '2025-10-03 08:18:02', '2025-10-03 08:18:02');

-- --------------------------------------------------------

--
-- Table structure for table `studio`
--

CREATE TABLE `studio` (
  `id_studio` int NOT NULL,
  `nama_studio` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `lokasi` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `kapasitas` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `studio`
--

INSERT INTO `studio` (`id_studio`, `nama_studio`, `lokasi`, `kapasitas`, `created_at`, `updated_at`) VALUES
(1, 'Studio Utama', 'Jakarta Pusat', 20, '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(2, 'Studio Mini', 'Jakarta Selatan', 8, '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(3, 'Studio Premium', 'Jakarta Barat', 30, '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(4, 'Studio Outdoor', 'Jakarta Timur', 15, '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(5, 'Studio Classic', 'Jakarta Utara', 12, '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(6, 'Studio Modern', 'Tangerang', 25, '2025-10-03 08:18:02', '2025-10-03 08:18:02'),
(7, 'Studio Neir', 'Banjarmasin', 20, '2025-11-25 12:51:01', '2025-11-25 12:51:01');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `fotografer`
--
ALTER TABLE `fotografer`
  ADD PRIMARY KEY (`id_fotografer`),
  ADD KEY `idx_nama` (`nama`),
  ADD KEY `idx_spesialisasi` (`spesialisasi`);

--
-- Indexes for table `jadwal`
--
ALTER TABLE `jadwal`
  ADD PRIMARY KEY (`id_sesi`),
  ADD KEY `idx_tanggal_waktu` (`tanggal_waktu`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_klien` (`id_klien`),
  ADD KEY `idx_fotografer` (`id_fotografer`),
  ADD KEY `idx_studio` (`id_studio`);

--
-- Indexes for table `klien`
--
ALTER TABLE `klien`
  ADD PRIMARY KEY (`id_klien`),
  ADD KEY `idx_nama` (`nama`),
  ADD KEY `idx_nomor_hp` (`nomor_hp`);

--
-- Indexes for table `studio`
--
ALTER TABLE `studio`
  ADD PRIMARY KEY (`id_studio`),
  ADD KEY `idx_nama_studio` (`nama_studio`),
  ADD KEY `idx_lokasi` (`lokasi`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `fotografer`
--
ALTER TABLE `fotografer`
  MODIFY `id_fotografer` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `jadwal`
--
ALTER TABLE `jadwal`
  MODIFY `id_sesi` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `klien`
--
ALTER TABLE `klien`
  MODIFY `id_klien` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `studio`
--
ALTER TABLE `studio`
  MODIFY `id_studio` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `jadwal`
--
ALTER TABLE `jadwal`
  ADD CONSTRAINT `jadwal_ibfk_1` FOREIGN KEY (`id_klien`) REFERENCES `klien` (`id_klien`) ON DELETE CASCADE,
  ADD CONSTRAINT `jadwal_ibfk_2` FOREIGN KEY (`id_fotografer`) REFERENCES `fotografer` (`id_fotografer`) ON DELETE CASCADE,
  ADD CONSTRAINT `jadwal_ibfk_3` FOREIGN KEY (`id_studio`) REFERENCES `studio` (`id_studio`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
