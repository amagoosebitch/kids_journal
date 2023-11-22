import boto3


def create_tables():
    dynamodb = boto3.resource('dynamodb', region_name='<ваш регион>')  # Замените на свой регион

    # Первый уровень
    organization_table = dynamodb.create_table(
        TableName='Organization',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'},
            {'AttributeName': 'start_education_time', 'AttributeType': 'N'},
            {'AttributeName': 'end_education_time', 'AttributeType': 'N'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Второй уровень
    group_table = dynamodb.create_table(
        TableName='Group',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'},
            {'AttributeName': 'organization_id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Третий уровень
    group_teacher_table = dynamodb.create_table(
        TableName='GroupTeacher',
        KeySchema=[
            {'AttributeName': 'group_id', 'KeyType': 'HASH'},
            {'AttributeName': 'teacher_id', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'group_id', 'AttributeType': 'S'},
            {'AttributeName': 'teacher_id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    group_child_table = dynamodb.create_table(
        TableName='GroupChild',
        KeySchema=[
            {'AttributeName': 'group_id', 'KeyType': 'HASH'},
            {'AttributeName': 'child_id', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'group_id', 'AttributeType': 'S'},
            {'AttributeName': 'child_id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    group_subject_table = dynamodb.create_table(
        TableName='GroupSubject',
        KeySchema=[
            {'AttributeName': 'group_id', 'KeyType': 'HASH'},
            {'AttributeName': 'subject_id', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'group_id', 'AttributeType': 'S'},
            {'AttributeName': 'subject_id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Четвертый уровень
    subject_table = dynamodb.create_table(
        TableName='Subject',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    child_table = dynamodb.create_table(
        TableName='Child',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Пятый уровень
    subject_presentation_table = dynamodb.create_table(
        TableName='SubjectPresentation',
        KeySchema=[
            {'AttributeName': 'subject_id', 'KeyType': 'HASH'},
            {'AttributeName': 'presentation_id', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'subject_id', 'AttributeType': 'S'},
            {'AttributeName': 'presentation_id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    child_skills_table = dynamodb.create_table(
        TableName='ChildSkills',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    child_parent_table = dynamodb.create_table(
        TableName='ChildParent',
        KeySchema=[
            {'AttributeName': 'child_id', 'KeyType': 'HASH'},
            {'AttributeName': 'parent_id', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'child_id', 'AttributeType': 'S'},
            {'AttributeName': 'parent_id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Шестой уровень
    presentation_table = dynamodb.create_table(
        TableName='Presentation',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    skill_db_table = dynamodb.create_table(
        TableName='SkillDB',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    skill_levels_db_table = dynamodb.create_table(
        TableName='SkillLevelsDB',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    parent_table = dynamodb.create_table(
        TableName='Parent',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    employee_table = dynamodb.create_table(
        TableName='Employee',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    schedule_table = dynamodb.create_table(
        TableName='Schedule',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Седьмой уровень
    roles_table = dynamodb.create_table(
        TableName='Roles',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    web_user_table = dynamodb.create_table(
        TableName='WebUser',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    tg_user_table = dynamodb.create_table(
        TableName='TGUser',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Привязки между таблицами
    # organization_table  # добавьте код для связей
    # group_table  # добавьте код для связей
    # и так далее

    return (
        organization_table, group_table, group_teacher_table, group_child_table, group_subject_table,
        subject_table, child_table, subject_presentation_table, child_skills_table, child_parent_table,
        presentation_table, skill_db_table, skill_levels_db_table, parent_table, employee_table, schedule_table,
        roles_table, web_user_table, tg_user_table
    )


if __name__ == '__main__':
    tables = create_tables()
    for table in tables:
        print("Статус таблицы:", table.table_status)
