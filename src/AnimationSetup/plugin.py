from enigma import setAnimation_current, setAnimation_speed
from Components.ActionMap import ActionMap
from Components.config import ConfigNumber, ConfigSelectionNumber, config
from Components.MenuList import MenuList
from Components.Sources.StaticText import StaticText
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Setup import Setup
from Plugins.Plugin import PluginDescriptor

from . import _

# default = slide to left
G_DEFAULT = {
		"current": 6,
		"speed": 20,
}
G_MAX_SPEED = 30

config.misc.window_animation_default = ConfigNumber(default=G_DEFAULT["current"])
config.misc.window_animation_speed = ConfigSelectionNumber(1, G_MAX_SPEED, 1, default=G_DEFAULT["speed"])


class AnimationSetupConfig(Setup):
	def __init__(self, session):
		Setup.__init__(self, session, "animationsetup", plugin="SystemPlugins/AnimationSetup", PluginLanguageDomain="AnimationSetup")
		self.onClose.append(self.onConfigClose)

	def onConfigClose(self):
		# Apply animation speed when closing
		setAnimation_speed(config.misc.window_animation_speed.value)


class AnimationSetupScreen(Screen):
	animationSetupItems = [
		{"idx": 0, "name": _("Disable Animations")},
		{"idx": 1, "name": _("Simple fade")},
		{"idx": 2, "name": _("Grow drop")},
		{"idx": 3, "name": _("Grow from left")},
		{"idx": 4, "name": _("Popup")},
		{"idx": 5, "name": _("Slide drop")},
		{"idx": 6, "name": _("Slide left to right")},
		{"idx": 7, "name": _("Slide top to bottom")},
		{"idx": 8, "name": _("Stripes")},
	]

	skin = """
		<screen name="AnimationSetup" position="center,center" size="580,400" title="Animation Setup">
			<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" zPosition="1" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" zPosition="1" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,0" size="140,40" zPosition="1" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" size="140,40" zPosition="1" alphatest="on" />

			<widget source="key_red" render="Label" position="0,0" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" foregroundColor="#ffffff" backgroundColor="#9f1313" transparent="1" />
			<widget source="key_green" render="Label" position="140,0" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" foregroundColor="#ffffff" backgroundColor="#1f771f" transparent="1" />
			<widget source="key_yellow" render="Label" position="280,0" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" foregroundColor="#ffffff" backgroundColor="#a08500" transparent="1" />
			<widget source="key_blue" render="Label" position="420,0" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" foregroundColor="#ffffff" backgroundColor="#18188b" transparent="1" />

			<widget name="list" position="10,60" size="560,364" scrollbarMode="showOnDemand" />
			<widget source="introduction" render="Label" position="0,370" size="560,40" zPosition="10" font="Regular;20" valign="center" backgroundColor="#25062748" transparent="1" />
		</screen>"""

	def __init__(self, session):

		self.skin = AnimationSetupScreen.skin
		Screen.__init__(self, session)

		self.animation_list = []

		self["introduction"] = StaticText(_("* current animation"))
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("Setting"))
		self["key_blue"] = StaticText(_("Preview"))

		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.keyclose,
				"save": self.ok,
				"ok": self.ok,
				"yellow": self.config,
				"blue": self.preview
			}, -3)

		self["list"] = MenuList(self.animation_list)

		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		items = []
		for x in self.animationSetupItems:
			key = x.get("idx", 0)
			name = x.get("name", "??")
			if key == config.misc.window_animation_default.value:
				name = f"* {name}"
			items.append((name, key))

		self["list"].setList(items)

	def ok(self):
		current = self["list"].getCurrent()
		if current:
			key = current[1]
			config.misc.window_animation_default.value = key
			config.misc.window_animation_default.save()
			setAnimation_current(key)
		self.close()

	def keyclose(self):
		setAnimation_current(config.misc.window_animation_default.value)
		setAnimation_speed(int(config.misc.window_animation_speed.value))
		self.close()

	def config(self):
		self.session.open(AnimationSetupConfig)

	def preview(self):
		current = self["list"].getCurrent()
		if current:
			setAnimation_current(current[1])
			self.session.open(MessageBox, current[0], MessageBox.TYPE_INFO, timeout=3)


def animation_setup_main(session, **kwargs):
	session.open(AnimationSetupScreen)


def start_animation_setup(menuid):
	if menuid != "system":
		return []

	return [(_("Animations"), animation_setup_main, "animation_setup", None)]


def session_animation_setup(session, reason, **kwargs):
	setAnimation_current(config.misc.window_animation_default.value)
	setAnimation_speed(int(config.misc.window_animation_speed.value))


def Plugins(**kwargs):
	return [
		PluginDescriptor(
			name="Animations",
			description="Setup UI animations",
			where=PluginDescriptor.WHERE_MENU,
			needsRestart=False,
			fnc=start_animation_setup),
		PluginDescriptor(
			where=PluginDescriptor.WHERE_SESSIONSTART,
			needsRestart=False,
			fnc=session_animation_setup)
	]
