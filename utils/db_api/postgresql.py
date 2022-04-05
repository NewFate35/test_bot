from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args, fetch: bool = False, fetchval: bool = False, fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        status BOOLEAN DEFAULT TRUE
        );
        """
        await self.execute(sql, execute=True)

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO Users(full_name, username, telegram_id) VALUES($1, $2, $3)"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_user(self, telegram_id):
        sql = f"SELECT * FROM Users WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users WHERE status=TRUE"
        return await self.execute(sql, fetch=True)

    async def update_user_status(self, new_status, telegram_id):
        sql = "UPDATE Users SET status=$1 WHERE telegram_id=$2"
        return await self.execute(sql, new_status, telegram_id, execute=True)
