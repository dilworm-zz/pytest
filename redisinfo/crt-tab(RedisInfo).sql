USE [UserInfo]
GO

/****** Object:  Table [dbo].[RedisInfo]    Script Date: 05/06/2016 01:49:41 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[RedisInfo](
	[redis_id] [smallint] NOT NULL,
	[redisdb_name] [nvarchar](32) NULL,
	[host] [nvarchar](50) NOT NULL,
	[port] [smallint] NOT NULL,
	[pid] [nchar](10) NOT NULL,
	[connected_clients] [smallint] NOT NULL,
	[keys] [bigint] NOT NULL,
	[keys_expires] [bigint] NOT NULL,
	[used_memory_human] [nvarchar](32) NOT NULL,
	[used_memory_peak_human] [decimal](12, 2) NOT NULL,
	[mem_fragmentation_ratio] [decimal](8, 2) NOT NULL,
	[instantaneous_ops_per_sec] [int] NOT NULL,
	[hit_rate] [decimal](3, 2) NOT NULL,
	[used_memory] [bigint] NOT NULL,
	[used_memory_rss] [bigint] NOT NULL,
	[used_memory_peak] [bigint] NOT NULL,
	[used_memory_lua] [bigint] NOT NULL,
	[expired_keys] [bigint] NOT NULL,
	[evicted_keys] [bigint] NOT NULL,
	[keyspace_hits] [bigint] NOT NULL,
	[keyspace_misses] [bigint] NOT NULL,
	[total_commands_processed] [bigint] NOT NULL,
	[pubsub_channels] [int] NOT NULL,
	[pubsub_patterns] [int] NOT NULL,
	[role] [nchar](10) NOT NULL,
	[connected_slaves] [tinyint] NOT NULL,
	[rdb_bgsave_in_progress] [tinyint] NOT NULL,
	[rdb_last_save_time] [datetime] NULL,
	[rdb_last_bgsave_status] [nchar](10) NOT NULL,
	[rdb_last_bgsave_time_sec] [int] NOT NULL,
	[aof_enabled] [tinyint] NOT NULL,
	[config_file] [nvarchar](300) NULL,
	[version] [nchar](10) NOT NULL,
	[uptime_in_seconds] [bigint] NOT NULL,
	[record_time] [datetime] NOT NULL
) ON [PRIMARY]

GO


