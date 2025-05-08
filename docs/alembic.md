# Managing Alembic

Alembic is a lightweight database migration tool for usage with SQLAlchemy. This document provides guidance on how to manage Alembic in this project.

## Configuration

The Alembic configuration file is located at the root of the project:

```
alembic.ini
```

This file contains the main configuration settings for Alembic, such as the database connection URL and the location of migration scripts.

## Directory Structure

The Alembic directory structure is as follows:

```
alembic/
    env.py          # Environment configuration for Alembic
    README          # Documentation for Alembic usage
    script.py.mako  # Template for generating migration scripts
    versions/       # Directory containing migration scripts
```

### Migration Scripts

Migration scripts are stored in the `alembic/versions/` directory. Each script is named with a unique identifier and a descriptive name, e.g., `5c626978d652_create_user.py`.

## Common Commands

Below are some common Alembic commands for managing database migrations:

### 1. Initialize Alembic

If Alembic is not already initialized, you can initialize it using the following command:

```bash
alembic init alembic
```

This creates the `alembic/` directory and the `alembic.ini` configuration file.

### 2. Create a New Migration

To create a new migration script, run:

```bash
alembic revision -m "<description>"
```

Replace `<description>` with a brief description of the migration, e.g., `add_users_table`.

If you want Alembic to automatically generate the migration script based on changes to your models, use:

```bash
alembic revision --autogenerate -m "<description>"
```

### 3. Apply Migrations

To apply all pending migrations to the database, run:

```bash
alembic upgrade head
```

You can also apply a specific migration by specifying its identifier:

```bash
alembic upgrade <revision_id>
```

### 4. Downgrade Migrations

To revert the last migration, run:

```bash
alembic downgrade -1
```

To revert to a specific migration, use:

```bash
alembic downgrade <revision_id>
```

### 5. Check Current Revision

To check the current migration version applied to the database, run:

```bash
alembic current
```

### 6. Show Migration History

To view the history of all migrations, run:

```bash
alembic history
```

## Best Practices

1. **Use Autogenerate**: When possible, use the `--autogenerate` flag to let Alembic detect changes in your models and generate migration scripts automatically.
2. **Review Scripts**: Always review the generated migration scripts to ensure they accurately reflect the intended changes.
3. **Test Migrations**: Test your migrations in a development or staging environment before applying them to production.
4. **Keep Migrations Organized**: Use descriptive names for migration scripts to make it easier to understand their purpose.

## Troubleshooting

- **Database Connection Issues**: Ensure the database connection URL in `alembic.ini` is correct.
- **Conflicting Migrations**: If multiple developers are working on migrations, coordinate to avoid conflicts and merge changes carefully.

For more information, refer to the [Alembic documentation](https://alembic.sqlalchemy.org/en/latest/).