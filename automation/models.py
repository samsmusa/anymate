from django.db import models


class AnnotationTagEntity(models.Model):
    name = models.CharField(unique=True, max_length=24)
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'annotation_tag_entity'


class AuthProviderSyncHistory(models.Model):
    providertype = models.CharField(db_column='providerType', max_length=32)
    runmode = models.TextField(db_column='runMode')
    status = models.TextField()
    startedat = models.DateTimeField(db_column='startedAt')
    endedat = models.DateTimeField(db_column='endedAt')
    scanned = models.IntegerField()
    created = models.IntegerField()
    updated = models.IntegerField()
    disabled = models.IntegerField()
    error = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_provider_sync_history'


class CredentialsEntity(models.Model):
    id = models.CharField(db_column='id', primary_key=True)
    name = models.CharField(max_length=128)
    data = models.TextField()
    type = models.CharField(max_length=128)
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')
    ismanaged = models.BooleanField(db_column='isManaged')

    class Meta:
        managed = False
        db_table = 'credentials_entity'


class EventDestinations(models.Model):
    destination = models.JSONField()
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'event_destinations'


class ExecutionAnnotationTags(models.Model):
    annotationid = models.ForeignKey('ExecutionAnnotations', models.DO_NOTHING,
                                     db_column='annotationId')
    tagid = models.ForeignKey(AnnotationTagEntity, models.DO_NOTHING, db_column='tagId')

    class Meta:
        managed = False
        db_table = 'execution_annotation_tags'


class ExecutionAnnotations(models.Model):
    executionid = models.OneToOneField('ExecutionEntity', models.DO_NOTHING,
                                       db_column='executionId')
    vote = models.CharField(max_length=6, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'execution_annotations'


class ExecutionData(models.Model):
    executionid = models.OneToOneField('ExecutionEntity', models.DO_NOTHING, db_column='executionId')
    workflowdata = models.TextField(db_column='workflowData')
    data = models.TextField()

    class Meta:
        managed = False
        db_table = 'execution_data'


class ExecutionEntity(models.Model):
    finished = models.BooleanField()
    mode = models.CharField()
    retryof = models.CharField(db_column='retryOf', blank=True, null=True)
    retrysuccessid = models.CharField(db_column='retrySuccessId', blank=True, null=True)
    startedat = models.DateTimeField(db_column='startedAt', blank=True, null=True)
    stoppedat = models.DateTimeField(db_column='stoppedAt', blank=True, null=True)
    waittill = models.DateTimeField(db_column='waitTill', blank=True, null=True)
    status = models.CharField()
    workflowid = models.ForeignKey('WorkflowEntity', models.DO_NOTHING,
                                   db_column='workflowId')
    deletedat = models.DateTimeField(db_column='deletedAt', blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')

    class Meta:
        managed = False
        db_table = 'execution_entity'


class ExecutionMetadata(models.Model):
    executionid = models.ForeignKey(ExecutionEntity, models.DO_NOTHING,
                                    db_column='executionId')
    key = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'execution_metadata'
        unique_together = (('executionid', 'key'),)


class Folder(models.Model):
    name = models.CharField(max_length=128)
    parentfolderid = models.ForeignKey('self', models.DO_NOTHING, db_column='parentFolderId', blank=True,
                                       null=True)
    projectid = models.ForeignKey('Project', models.DO_NOTHING, db_column='projectId')
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'folder'
        unique_together = (('projectid', 'id'),)


class FolderTag(models.Model):
    folderid = models.ForeignKey(Folder, models.DO_NOTHING, db_column='folderId')
    tagid = models.ForeignKey('TagEntity', models.DO_NOTHING, db_column='tagId')

    class Meta:
        managed = False
        db_table = 'folder_tag'


class InsightsByPeriod(models.Model):
    metaid = models.ForeignKey('InsightsMetadata', models.DO_NOTHING, db_column='metaId')
    type = models.IntegerField(db_comment='0: time_saved_minutes, 1: runtime_milliseconds, 2: success, 3: failure')
    value = models.IntegerField()
    periodunit = models.IntegerField(db_column='periodUnit',
                                     db_comment='0: hour, 1: day, 2: week')
    periodstart = models.DateTimeField(db_column='periodStart', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'insights_by_period'
        unique_together = (('periodstart', 'type', 'periodunit', 'metaid'),)


class InsightsMetadata(models.Model):
    metaid = models.AutoField(db_column='metaId', primary_key=True)
    workflowid = models.OneToOneField('WorkflowEntity', models.DO_NOTHING,
                                      db_column='workflowId', blank=True,
                                      null=True)
    projectid = models.ForeignKey('Project', models.DO_NOTHING, db_column='projectId', blank=True,
                                  null=True)
    workflowname = models.CharField(db_column='workflowName', max_length=128)
    projectname = models.CharField(db_column='projectName', max_length=255)

    class Meta:
        managed = False
        db_table = 'insights_metadata'


class InsightsRaw(models.Model):
    metaid = models.ForeignKey(InsightsMetadata, models.DO_NOTHING, db_column='metaId')
    type = models.IntegerField(db_comment='0: time_saved_minutes, 1: runtime_milliseconds, 2: success, 3: failure')
    value = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'insights_raw'


class InstalledNodes(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    latestversion = models.IntegerField(db_column='latestVersion')
    package = models.ForeignKey('InstalledPackages', models.DO_NOTHING, db_column='package')

    class Meta:
        managed = False
        db_table = 'installed_nodes'


class InstalledPackages(models.Model):
    packagename = models.CharField(db_column='packageName', max_length=214)
    installedversion = models.CharField(db_column='installedVersion', max_length=50)
    authorname = models.CharField(db_column='authorName', max_length=70, blank=True,
                                  null=True)
    authoremail = models.CharField(db_column='authorEmail', max_length=70, blank=True,
                                   null=True)
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'installed_packages'


class InvalidAuthToken(models.Model):
    token = models.CharField(max_length=512)
    expiresat = models.DateTimeField(db_column='expiresAt')

    class Meta:
        managed = False
        db_table = 'invalid_auth_token'


class Migrations(models.Model):
    timestamp = models.BigIntegerField()
    name = models.CharField()

    class Meta:
        managed = False
        db_table = 'migrations'


class ProcessedData(models.Model):
    workflowid = models.ForeignKey('WorkflowEntity', models.DO_NOTHING,
                                   db_column='workflowId')
    context = models.CharField(max_length=255)
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'processed_data'


class Project(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=36)
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')
    icon = models.TextField(blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project'


class ProjectRelation(models.Model):
    projectid = models.ForeignKey(Project, models.DO_NOTHING, db_column='projectId')
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')
    role = models.CharField()
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = (('project_relation', "userId"),)


class Settings(models.Model):
    key = models.CharField(max_length=255)
    value = models.TextField()
    loadonstartup = models.BooleanField(db_column='loadOnStartup')

    class Meta:
        managed = False
        db_table = 'settings'


class SharedCredentials(models.Model):
    credentialsid = models.ForeignKey(CredentialsEntity, models.DO_NOTHING,
                                      db_column='credentialsId')
    projectid = models.ForeignKey(Project, models.DO_NOTHING, db_column='projectId')
    role = models.TextField()
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'shared_credentials'


class SharedWorkflow(models.Model):
    workflowid = models.ForeignKey('WorkflowEntity', models.DO_NOTHING,
                                   db_column='workflowId')
    projectid = models.ForeignKey(Project, models.DO_NOTHING, db_column='projectId')
    role = models.TextField()
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'shared_workflow'


class TagEntity(models.Model):
    name = models.CharField(unique=True, max_length=24)
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'tag_entity'


class TestCaseExecution(models.Model):
    testrunid = models.ForeignKey('TestRun', models.DO_NOTHING, db_column='testRunId')
    executionid = models.ForeignKey(ExecutionEntity, models.DO_NOTHING, db_column='executionId', blank=True,
                                    null=True)
    status = models.CharField()
    runat = models.DateTimeField(db_column='runAt', blank=True, null=True)
    completedat = models.DateTimeField(db_column='completedAt', blank=True, null=True)
    errorcode = models.CharField(db_column='errorCode', blank=True, null=True)
    errordetails = models.TextField(db_column='errorDetails', blank=True,
                                    null=True)
    metrics = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')
    inputs = models.TextField(blank=True, null=True)
    outputs = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_case_execution'


class TestRun(models.Model):
    workflowid = models.ForeignKey('WorkflowEntity', models.DO_NOTHING,
                                   db_column='workflowId')
    status = models.CharField()
    errorcode = models.CharField(db_column='errorCode', blank=True, null=True)
    errordetails = models.TextField(db_column='errorDetails', blank=True,
                                    null=True)
    runat = models.DateTimeField(db_column='runAt', blank=True, null=True)
    completedat = models.DateTimeField(db_column='completedAt', blank=True, null=True)
    metrics = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'test_run'


class User(models.Model):
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    firstname = models.CharField(db_column='firstName', max_length=32, blank=True,
                                 null=True)
    lastname = models.CharField(db_column='lastName', max_length=32, blank=True,
                                null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    personalizationanswers = models.TextField(db_column='personalizationAnswers', blank=True,
                                              null=True)
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')
    settings = models.TextField(blank=True, null=True)
    disabled = models.BooleanField()
    mfaenabled = models.BooleanField(db_column='mfaEnabled')
    mfasecret = models.TextField(db_column='mfaSecret', blank=True, null=True)
    mfarecoverycodes = models.TextField(db_column='mfaRecoveryCodes', blank=True,
                                        null=True)
    role = models.TextField()
    lastactiveat = models.DateField(db_column='lastActiveAt', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserApiKeys(models.Model):
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')
    label = models.CharField(max_length=100)
    apikey = models.CharField(db_column='apiKey', unique=True)
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')
    scopes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_api_keys'
        unique_together = (('userid', 'label'),)


class Variables(models.Model):
    key = models.CharField(unique=True, max_length=50)
    type = models.CharField(max_length=50)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'variables'


class WebhookEntity(models.Model):
    webhookpath = models.CharField(db_column='webhookPath')
    method = models.CharField()
    node = models.CharField()
    webhookid = models.CharField(db_column='webhookId', blank=True, null=True)
    pathlength = models.IntegerField(db_column='pathLength', blank=True, null=True)
    workflowid = models.ForeignKey('WorkflowEntity', models.DO_NOTHING,
                                   db_column='workflowId')

    class Meta:
        managed = False
        db_table = 'webhook_entity'


class WorkflowEntity(models.Model):
    id = models.CharField(db_column='id', primary_key=True)
    name = models.CharField(max_length=128)
    active = models.BooleanField()
    nodes = models.TextField()
    connections = models.TextField()
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')
    settings = models.TextField(blank=True, null=True)
    staticdata = models.TextField(db_column='staticData', blank=True,
                                  null=True)
    pindata = models.TextField(db_column='pinData', blank=True,
                               null=True)
    versionid = models.CharField(db_column='versionId', max_length=36, blank=True,
                                 null=True)
    triggercount = models.IntegerField(db_column='triggerCount')
    meta = models.TextField(blank=True, null=True)
    parentfolderid = models.ForeignKey(Folder, models.DO_NOTHING, db_column='parentFolderId', blank=True,
                                       null=True)
    isarchived = models.BooleanField(db_column='isArchived')

    class Meta:
        managed = False
        db_table = 'workflow_entity'


class WorkflowHistory(models.Model):
    versionid = models.CharField(db_column='versionId', max_length=36)
    workflowid = models.ForeignKey(WorkflowEntity, models.DO_NOTHING,
                                   db_column='workflowId')
    authors = models.CharField(max_length=255)
    createdat = models.DateTimeField(db_column='createdAt')
    updatedat = models.DateTimeField(db_column='updatedAt')
    nodes = models.TextField()
    connections = models.TextField()

    class Meta:
        managed = False
        db_table = 'workflow_history'


class WorkflowStatistics(models.Model):
    count = models.IntegerField(blank=True, null=True)
    latestevent = models.DateTimeField(db_column='latestEvent', blank=True, null=True)
    name = models.CharField(max_length=128)
    workflowid = models.ForeignKey(WorkflowEntity, models.DO_NOTHING,
                                   db_column='workflowId')
    rootcount = models.IntegerField(db_column='rootCount', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'workflow_statistics'



class WorkflowsTags(models.Model):
    workflowid = models.ForeignKey(WorkflowEntity, models.DO_NOTHING,
                                   db_column='workflowId')
    tagid = models.ForeignKey(TagEntity, models.DO_NOTHING, db_column='tagId')

    class Meta:
        managed = False
        db_table = 'workflows_tags'
