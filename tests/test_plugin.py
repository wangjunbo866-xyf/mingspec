"""Check the plugin directory and the existing direct-Skills route."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {'ming-spec', 'ming-tickets', 'ming-archive', 'ming-runbook'}


class PluginPackageTests(unittest.TestCase):
    def test_repository_catalog_resolves_portable_plugin(self):
        manifest = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['$schema'],
                         'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json')
        self.assertEqual(manifest['name'], 'mingspec')
        self.assertRegex(manifest['version'], r'^\d+\.\d+\.\d+$')
        self.assertNotIn('skills', manifest)  # Portable format uses fixed skills/.
        self.assertNotIn('mcpServers', manifest)
        extension = manifest['extensions']['com.openai']
        self.assertEqual(set(extension), {'interface'})
        self.assertLessEqual(len(extension['interface']['shortDescription']), 30)
        self.assertEqual(extension['interface']['capabilities'], [])
        entries = {p.parent.name for p in (ROOT / 'skills').glob('*/SKILL.md')}
        self.assertEqual(entries, SKILLS)
        catalog = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text(
            encoding='utf-8'))
        self.assertEqual(len(catalog['plugins']), 1)
        plugin = catalog['plugins'][0]
        self.assertEqual(plugin['name'], manifest['name'])
        self.assertEqual(plugin['source']['source'], 'local')
        self.assertEqual((ROOT / plugin['source']['path']).resolve(), ROOT)
        self.assertEqual(plugin['policy']['installation'], 'AVAILABLE')

    def test_relocated_resources_initialize_without_overwriting_target(self):
        with tempfile.TemporaryDirectory(prefix='mingspec plugin ') as directory:
            product = Path(directory) / 'moved product'
            product.mkdir()
            for name in ('scripts', 'templates', 'skills'):
                shutil.copytree(ROOT / name, product / name)
            shutil.copy2(ROOT / 'onboarding.md', product / 'onboarding.md')
            shutil.copy2(ROOT / 'plugin.json', product / 'plugin.json')
            target = Path(directory) / 'business project'
            target.mkdir()
            original = b'# Existing Project\n\nKeep this decision.\n'
            (target / 'AGENTS.md').write_bytes(original)
            command = [sys.executable, '-B', str(product / 'scripts/mingspec'),
                       'init', str(target)]
            result = subprocess.run(command, cwd=target, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((target / 'AGENTS.md').read_bytes(), original)
            for name in ('readme.md', 'specs/readme.md', 'runbook/readme.md',
                         'vendor/readme.md'):
                self.assertEqual((target / 'mingspec' / name).read_bytes(),
                                 (product / 'templates/mingspec' / name).read_bytes())
            before = {p.relative_to(target): p.read_bytes()
                      for p in target.rglob('*') if p.is_file()}
            again = subprocess.run(command, cwd=target, capture_output=True, text=True)
            self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
            self.assertEqual(before, {p.relative_to(target): p.read_bytes()
                                     for p in target.rglob('*') if p.is_file()})
            self.assertFalse((target / 'plugin.json').exists())
            self.assertFalse((target / 'skills').exists())
            # Archive shares the specification resources, including after moving
            # the product and entering through a project's direct-Skills links.
            links = target / '.agents/skills'
            links.mkdir(parents=True)
            for name in SKILLS:
                (links / name).symlink_to(product / 'skills' / name,
                                         target_is_directory=True)
            archive = (links / 'ming-archive/SKILL.md').resolve()
            self.assertEqual(archive, product / 'skills/ming-archive/SKILL.md')
            for resource in ('spec-anchors.md', 'business-map.md', 'spec-home.md'):
                shared = archive.parent / '../ming-spec/references' / resource
                self.assertEqual(shared.read_bytes(),
                                 (ROOT / 'skills/ming-spec/references' / resource).read_bytes())
            self.assertEqual({p.name for p in links.iterdir()}, SKILLS)

    @unittest.skipUnless(hasattr(Path, 'symlink_to'), 'symbolic links unavailable')
    def test_direct_skill_links_resolve_the_same_resources(self):
        with tempfile.TemporaryDirectory(prefix='mingspec direct ') as directory:
            target = Path(directory) / '.agents/skills'
            target.mkdir(parents=True)
            for name in SKILLS:
                (target / name).symlink_to(ROOT / 'skills' / name, target_is_directory=True)
                actual = (target / name / 'SKILL.md').resolve()
                self.assertEqual(actual, ROOT / 'skills' / name / 'SKILL.md')
                package = actual.parents[2]
                for resource in ('onboarding.md', 'scripts/mingspec', 'templates/AGENTS.md',
                                 'skills/ming-spec/assets/spec.md',
                                 'skills/ming-tickets/assets/tasks.md',
                                 'skills/ming-spec/references/spec-anchors.md',
                                 'skills/ming-spec/references/business-map.md'):
                    self.assertTrue((package / resource).is_file(), resource)


if __name__ == '__main__':
    unittest.main()
