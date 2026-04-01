from setuptools import setup
import setup_translate

pkg = 'SystemPlugins.AnimationSetup'
setup(name='enigma2-plugin-systemplugins-animation-setup',
       version='3.0',
       description='animation-setup',
       package_dir={pkg: 'AnimationSetup'},
       packages=[pkg],
       package_data={pkg: ['images/*.png', '*.png', '*.xml', 'locale/*/LC_MESSAGES/*.mo']},
       cmdclass=setup_translate.cmdclass,  # for translation
      )
