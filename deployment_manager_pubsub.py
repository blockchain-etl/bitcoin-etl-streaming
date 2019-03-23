def GenerateConfig(context):
    resources = []

    chains = ['bitcoin', 'bitcoin_cash', 'dogecoin', 'litecoin', 'dash', 'zcash']

    for chain in chains:
        topic_name_prefix = 'crypto_' + chain
        subscription_name_prefix = 'crypto_' + chain + '.dataflow.bigquery'
        # 7 days
        message_retention_duration = '604800s'

        # blocks
        blocks_topic_name = topic_name_prefix + '.blocks'
        blocks_topic_resource_name = topic_name_prefix + '.blocks'.replace('.', '-')
        blocks_subscription_name = subscription_name_prefix + '.blocks'
        blocks_subscription_resource_name = (subscription_name_prefix + '.blocks').replace('.', '-')
        resources.append({
            'name': blocks_topic_resource_name,
            'type': 'pubsub.v1.topic',
            'properties': {
                'topic': blocks_topic_name
            }
        })
        resources.append({
            'name': blocks_subscription_resource_name,
            'type': 'pubsub.v1.subscription',
            'properties': {
                'subscription': blocks_subscription_name,
                'topic': '$(ref.' + blocks_topic_resource_name + '.name)',
                'ackDeadlineSeconds': 30,
                'retainAckedMessages': True,
                'messageRetentionDuration': message_retention_duration,
                'expirationPolicy': {
                }
            }
        })

        # transactions
        transactions_topic_name = topic_name_prefix + '.transactions'
        transactions_topic_resource_name = topic_name_prefix + '.transactions'.replace('.', '-')
        transactions_subscription_name = subscription_name_prefix + '.transactions'
        transactions_subscription_resource_name = (subscription_name_prefix + '.transactions').replace('.', '-')
        resources.append({
            'name': transactions_topic_resource_name,
            'type': 'pubsub.v1.topic',
            'properties': {
                'topic': transactions_topic_name
            }
        })
        resources.append({
            'name': transactions_subscription_resource_name,
            'type': 'pubsub.v1.subscription',
            'properties': {
                'subscription': transactions_subscription_name,
                'topic': '$(ref.' + transactions_topic_resource_name + '.name)',
                'ackDeadlineSeconds': 30,
                'retainAckedMessages': True,
                'messageRetentionDuration': message_retention_duration,
                'expirationPolicy': {
                }
            }
        })

    return {'resources': resources}
