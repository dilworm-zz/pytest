-- ================================================
-- Template generated from Template Explorer using:
-- Create Procedure (New Menu).SQL
--
-- Use the Specify Values for Template Parameters 
-- command (Ctrl-Shift-M) to fill in the parameter 
-- values below.
--
-- This block of comments will not be included in
-- the definition of the procedure.
-- ================================================
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		YGD
-- Create date: 2016-5-5
-- Description:	Insert redisinfo record
-- =============================================
CREATE PROCEDURE GSP_InsertRedisInfo
			(@redis_id smallint
           ,@redisdb_name nvarchar(32)
           ,@host nvarchar(50)
           ,@port smallint
           ,@pid nchar(10)
           ,@connected_clients smallint
           ,@keys bigint
           ,@keys_expires bigint
           ,@used_memory_human nvarchar(32)
           ,@used_memory_peak_human decimal(12,2)
           ,@mem_fragmentation_ratio decimal(8,2)
           ,@instantaneous_ops_per_sec int
           ,@hit_rate decimal(3,2)
           ,@used_memory bigint
           ,@used_memory_rss bigint
           ,@used_memory_peak bigint
           ,@used_memory_lua bigint
           ,@expired_keys bigint
           ,@evicted_keys bigint
           ,@keyspace_hits bigint
           ,@keyspace_misses bigint
           ,@total_commands_processed bigint
           ,@pubsub_channels int
           ,@pubsub_patterns int
           ,@role nchar(10)
           ,@connected_slaves tinyint
           ,@rdb_bgsave_in_progress tinyint
           ,@rdb_last_save_time datetime
           ,@rdb_last_bgsave_status nchar(10)
           ,@rdb_last_bgsave_time_sec int
           ,@aof_enabled tinyint 
           ,@config_file nvarchar(300)
           ,@version nchar(10)
           ,@uptime_in_seconds bigint)

AS
BEGIN
	SET NOCOUNT ON;

 INSERT INTO [UserInfo].[dbo].[RedisInfo]
           ([redis_id]
           ,[redisdb_name]
           ,[host]
           ,[port]
           ,[pid]
           ,[connected_clients]
           ,[keys]
           ,[keys_expires]
           ,[used_memory_human]
           ,[used_memory_peak_human]
           ,[mem_fragmentation_ratio]
           ,[instantaneous_ops_per_sec]
           ,[hit_rate]
           ,[used_memory]
           ,[used_memory_rss]
           ,[used_memory_peak]
           ,[used_memory_lua]
           ,[expired_keys]
           ,[evicted_keys]
           ,[keyspace_hits]
           ,[keyspace_misses]
           ,[total_commands_processed]
           ,[pubsub_channels]
           ,[pubsub_patterns]
           ,[role]
           ,[connected_slaves]
           ,[rdb_bgsave_in_progress]
           ,[rdb_last_save_time]
           ,[rdb_last_bgsave_status]
           ,[rdb_last_bgsave_time_sec]
           ,[aof_enabled]
           ,[config_file]
           ,[version]
           ,[uptime_in_seconds]
           ,[record_time])
     VALUES
(@redis_id
           ,@redisdb_name
           ,@host
           ,@port
           ,@pid
           ,@connected_clients
           ,@keys
           ,@keys_expires
           ,@used_memory_human
           ,@used_memory_peak_human
           ,@mem_fragmentation_ratio
           ,@instantaneous_ops_per_sec
           ,@hit_rate
           ,@used_memory
           ,@used_memory_rss
           ,@used_memory_peak
           ,@used_memory_lua
           ,@expired_keys
           ,@evicted_keys
           ,@keyspace_hits
           ,@keyspace_misses
           ,@total_commands_processed
           ,@pubsub_channels
           ,@pubsub_patterns
           ,@role
           ,@connected_slaves
           ,@rdb_bgsave_in_progress
           ,@rdb_last_save_time
           ,@rdb_last_bgsave_status
           ,@rdb_last_bgsave_time_sec
           ,@aof_enabled
           ,@config_file
           ,@version
           ,@uptime_in_seconds
           ,GETDATE())


END

