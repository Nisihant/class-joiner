from django.db import models
from django.contrib.auth.models import User
# from codeShare.models import Code
from datetime import datetime
from django.utils import timezone

defaultSettings = dict({
    'selectionStyle': 'line',
    'highlightActiveLine': True,
    'highlightSelectedWord': True,
    'readOnly': False, 
    'copyWithEmptySelection': False, 
    'cursorStyle': 'ace', 
    'mergeUndoDeltas': True, 
    'behavioursEnabled': True, 
    'wrapBehavioursEnabled': True, 
    'enableAutoIndent': True, 
    'showLineNumbers': True, 
    'hScrollBarAlwaysVisible': False, 
    'vScrollBarAlwaysVisible': False, 
    'highlightGutterLine': True,
    'animatedScroll': False, 
    'showInvisibles': False, 
    'showPrintMargin': True, 
    'printMarginColumn': 80, 
    'printMargin': 80, 'fadeFoldWidgets': False, 
    'showFoldWidgets': True, 
    'displayIndentGuides': True, 
    'showGutter': True, 
    'fontSize': 24, 
    'scrollPastEnd': 0, 
    'theme': 'ace/theme/cobalt', 
    'maxPixelHeight': 0, 
    'useTextareaForIME': True, 
    'scrollSpeed': 2, 
    'dragDelay': 0, 
    'dragEnabled': True, 
    'focusTimeout': 0, 
    'tooltipFollowsMouse': True, 
    'firstLineNumber': 1, 
    'overwrite': False, 
    'newLineMode': 'auto', 
    'useWorker': True, 
    'useSoftTabs': True, 
    'navigateWithinSoftTabs': False, 
    'tabSize': 4, 
    'wrap': 'off', 
    'indentedSoftWrap': True, 
    'foldStyle': 'markbegin', 
    'mode': 'ace/mode/python', 
    'enableMultiselect': True, 
    'enableBlockSelect': True, 
    'enableBasicAutocompletion': True, 
    'enableLiveAutocompletion': True, 
    'enableSnippets': True,
    'minLines': 30,
    'maxLines': 60,
})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # codes = models.ManyToManyField(Code, blank=True)
    lastSettings = models.JSONField(default=defaultSettings)
    lastMode = models.BooleanField(default=True)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now(tz=timezone.utc))

    def __str__(self):
        return self.user.username
