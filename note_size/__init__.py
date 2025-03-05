from aqt import gui_hooks

from .common.collection_holder import CollectionHolder
from .ui.profile_hook import ProfileHook

collection_holder: CollectionHolder = CollectionHolder()
profile_hook: ProfileHook = ProfileHook(collection_holder)

gui_hooks.collection_did_load.append(lambda col: collection_holder.set_collection(col))
gui_hooks.profile_did_open.append(lambda: profile_hook.initialize())
gui_hooks.profile_will_close.append(lambda: profile_hook.shutdown())
