-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Хост: localhost
-- Время создания: Окт 10 2014 г., 15:03
-- Версия сервера: 5.5.38-0ubuntu0.14.04.1
-- Версия PHP: 5.5.9-1ubuntu4.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- База данных: `cmdb`
--

-- --------------------------------------------------------

--
-- Структура таблицы `dictionary`
--

CREATE TABLE IF NOT EXISTS `dictionary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- Дамп данных таблицы `dictionary`
--

INSERT INTO `dictionary` (`id`, `name`) VALUES
(1, 'RAM'),
(2, 'OperationSystem');

-- --------------------------------------------------------

--
-- Структура таблицы `dictionary_values`
--

CREATE TABLE IF NOT EXISTS `dictionary_values` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dict_id` int(11) NOT NULL,
  `value` varchar(256) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=7 ;

--
-- Дамп данных таблицы `dictionary_values`
--

INSERT INTO `dictionary_values` (`id`, `dict_id`, `value`) VALUES
(1, 2, 'RHEL 5.5 x64'),
(2, 2, 'RHEL 6.5 x64'),
(3, 2, 'RHEL 7.0 x64'),
(4, 2, 'CentOS Linux 6.5 x64'),
(5, 2, 'CentOS Linux 7.0 x64'),
(6, 2, 'Windos Server 2008 R2 x64');

-- --------------------------------------------------------

--
-- Структура таблицы `properties`
--

CREATE TABLE IF NOT EXISTS `properties` (
  `prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL,
  `prop_name` varchar(256) CHARACTER SET latin1 NOT NULL,
  `dictionare_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`prop_id`),
  UNIQUE KEY `uuid` (`prop_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=10 ;

--
-- Дамп данных таблицы `properties`
--

INSERT INTO `properties` (`prop_id`, `type_id`, `prop_name`, `dictionare_id`) VALUES
(1, 1, 'UUID', NULL),
(2, 1, 'NAME', NULL),
(3, 1, 'CPU', NULL),
(4, 1, 'RAM', NULL),
(5, 1, 'HDD', NULL),
(6, 1, 'hostname', NULL),
(7, 1, 'MAC Address', NULL),
(8, 1, 'IP Address', NULL),
(9, 1, 'Owner', NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `resources`
--

CREATE TABLE IF NOT EXISTS `resources` (
  `uuid` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL,
  `cteate_date` datetime NOT NULL,
  `update_date` datetime NOT NULL,
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `uuid` (`uuid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- Дамп данных таблицы `resources`
--

INSERT INTO `resources` (`uuid`, `type_id`, `cteate_date`, `update_date`) VALUES
(1, 1, '2014-10-08 00:00:00', '2014-10-08 00:00:00'),
(2, 1, '2014-10-09 00:00:00', '2014-10-09 00:00:00');

-- --------------------------------------------------------

--
-- Структура таблицы `types`
--

CREATE TABLE IF NOT EXISTS `types` (
  `type_id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(50) CHARACTER SET latin1 NOT NULL,
  `worker_id` int(11) NOT NULL,
  PRIMARY KEY (`type_id`),
  UNIQUE KEY `uuid` (`type_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- Дамп данных таблицы `types`
--

INSERT INTO `types` (`type_id`, `type_name`, `worker_id`) VALUES
(1, 'Virtual Machin', 0),
(2, 'ShareFolders', 0);

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `pass` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `cookie` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `login`, `pass`, `cookie`) VALUES
(2, 'admin@mail.ru', '123456', 'ade479d7abd084eafe57207cd7978baa');

-- --------------------------------------------------------

--
-- Структура таблицы `values`
--

CREATE TABLE IF NOT EXISTS `values` (
  `value_id` int(11) NOT NULL AUTO_INCREMENT,
  `prop_id` int(11) NOT NULL,
  `uuid` int(11) NOT NULL,
  `value` varchar(256) CHARACTER SET latin1 NOT NULL,
  `last_user` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `up_date` datetime NOT NULL,
  `last_value` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`value_id`),
  UNIQUE KEY `value_id` (`value_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=12 ;

--
-- Дамп данных таблицы `values`
--

INSERT INTO `values` (`value_id`, `prop_id`, `uuid`, `value`, `last_user`, `up_date`, `last_value`) VALUES
(1, 1, 1, '4232447b-b651-7fb6-0a65-a08c74773dcb', 'akrush', '2014-10-07 00:00:00', 1),
(2, 2, 1, 'CMDB', 'akrush', '2014-10-07 00:00:00', 1),
(3, 3, 1, '1', 'akrush', '2014-10-07 00:00:00', 1),
(4, 4, 1, '1024', 'akrush', '2014-10-07 00:00:00', 1),
(5, 6, 1, 'cmdb.at-consulting.ru', 'akrush', '2014-10-07 00:00:00', 1),
(6, 7, 1, '00:50:56:b2:36:a3', 'akrush', '2014-10-07 00:00:00', 1),
(7, 8, 1, '192.168.15.183', 'akrush', '2014-10-07 00:00:00', 0),
(8, 9, 1, 'kav@at-consulting.ru', 'akrush', '2014-10-07 00:00:00', 1),
(9, 9, 1, 'vkarmanov@at-consulting.ru', 'akrush', '2014-10-07 00:00:00', 1),
(10, 8, 1, '192.168.15.184', 'akrush', '2014-10-07 15:22:23', 0),
(11, 8, 1, '192.168.15.180', 'akrush', '2014-10-08 08:22:23', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `worker`
--

CREATE TABLE IF NOT EXISTS `worker` (
  `worker_id` int(11) NOT NULL AUTO_INCREMENT,
  `worker_path` varchar(256) CHARACTER SET latin1 NOT NULL,
  `worker_values_id` int(11) NOT NULL,
  PRIMARY KEY (`worker_id`),
  UNIQUE KEY `worker_id` (`worker_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Структура таблицы `worker_values`
--

CREATE TABLE IF NOT EXISTS `worker_values` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `worker_id` int(11) NOT NULL,
  `value` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
