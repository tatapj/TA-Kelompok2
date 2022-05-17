-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 17, 2022 at 03:38 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cuaca`
--

-- --------------------------------------------------------

--
-- Table structure for table `captures`
--

CREATE TABLE `captures` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `cuaca_id` bigint(20) UNSIGNED NOT NULL,
  `status_capture` int(11) NOT NULL DEFAULT 0,
  `show` int(11) NOT NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `captures`
--

INSERT INTO `captures` (`id`, `cuaca_id`, `status_capture`, `show`, `created_at`, `updated_at`) VALUES
(1, 1, 1, 1, '2022-05-06 04:30:04', '2022-05-06 07:20:37');

-- --------------------------------------------------------

--
-- Table structure for table `cuacas`
--

CREATE TABLE `cuacas` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `nama_gambar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `recognize` int(11) NOT NULL DEFAULT 0,
  `kondisi_cuaca` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `kondisi_jendela` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0',
  `showed` int(11) NOT NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `cuacas`
--

INSERT INTO `cuacas` (`id`, `nama_gambar`, `recognize`, `kondisi_cuaca`, `kondisi_jendela`, `showed`, `created_at`, `updated_at`) VALUES
(1, 'default.jpg', 0, NULL, '0', 0, '2022-05-06 04:30:04', '2022-05-06 04:30:04');

-- --------------------------------------------------------

--
-- Table structure for table `histories`
--

CREATE TABLE `histories` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `cuaca_id` bigint(20) UNSIGNED NOT NULL,
  `kondisi_cuaca` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ket` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `locations`
--

CREATE TABLE `locations` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `location` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `locations`
--

INSERT INTO `locations` (`id`, `location`, `created_at`, `updated_at`) VALUES
(1, '<iframe width=\"600\" height=\"500\" id=\"gmap_canvas\" src=\"https://maps.google.com/maps?q=Institut%20teknologi%20del&t=&z=13&ie=UTF8&iwloc=&output=embed\" frameborder=\"0\" scrolling=\"no\" marginheight=\"0\" marginwidth=\"0\"></iframe>', '2022-05-06 04:30:04', '2022-05-06 08:40:03');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `captures`
--
ALTER TABLE `captures`
  ADD PRIMARY KEY (`id`),
  ADD KEY `captures_cuaca_id_foreign` (`cuaca_id`);

--
-- Indexes for table `cuacas`
--
ALTER TABLE `cuacas`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `histories`
--
ALTER TABLE `histories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `histories_cuaca_id_foreign` (`cuaca_id`);

--
-- Indexes for table `locations`
--
ALTER TABLE `locations`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `captures`
--
ALTER TABLE `captures`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `cuacas`
--
ALTER TABLE `cuacas`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `histories`
--
ALTER TABLE `histories`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `locations`
--
ALTER TABLE `locations`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `captures`
--
ALTER TABLE `captures`
  ADD CONSTRAINT `captures_cuaca_id_foreign` FOREIGN KEY (`cuaca_id`) REFERENCES `cuacas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `histories`
--
ALTER TABLE `histories`
  ADD CONSTRAINT `histories_cuaca_id_foreign` FOREIGN KEY (`cuaca_id`) REFERENCES `cuacas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
