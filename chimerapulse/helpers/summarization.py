"""This is a helper file for core.language.conversation_summarization capability

Reference:
    Lists of conversation summarization tasks: https://learn.microsoft.com/en-us/rest/api/language/conversation-analysis-runtime/submit-job?view=rest-language-2023-04-01&tabs=HTTP#summaryaspect
"""
convo_summarization_tasks = ['chapterTitle', 'issue', 'narrative', 'resolution']

def __validate_tasks_type(tasks):
    if tasks == 'all':
        return convo_summarization_tasks

    if type(tasks) is not bytearray:
        raise ValueError('ERROR: Parameter tasks datatype should be an array') 

    return tasks


def create_tasks(tasks='all'):
    tasks_obj = []

    validated_tasks = __validate_tasks_type(tasks)

    for task in validated_tasks:
        if task not in convo_summarization_tasks:
            raise ValueError('ERROR: task value not allowed.') 

        tasks_obj.append({
            "taskName": f'{task} task',
            "kind": "ConversationalSummarizationTask",
            "parameters": {"summaryAspects": [task]}
        })

    return tasks_obj
