"""Advisory physical-line counts for explicitly selected main specifications."""

from pathlib import Path


def is_main_spec(spec):
    parts = spec.split('/')
    return (len(parts) == 5 and parts[:2] == ['mingspec', 'specs']
            and parts[-1] == 'spec.md'
            and all(part and part not in ('.', '..') for part in parts)
            and '\\' not in spec)


def check_spec_size(root, spec):
    if not is_main_spec(spec):
        print('参数错误：--spec 必须是 mingspec/specs/<domain>/<module>/spec.md 相对路径。')
        return 2
    try:
        project = Path(root).resolve(strict=True)
        if not project.is_dir():
            raise ValueError('项目根不是目录')
    except (OSError, ValueError, RuntimeError) as exc:
        print(f'项目根无效：{exc}')
        return 1
    try:
        path = (project / spec).resolve(strict=True)
        relative = path.relative_to(project).as_posix()
        if not is_main_spec(relative):
            raise ValueError('实际目标不是规范模块主规格')
        if not path.is_file():
            raise ValueError('目标不是普通文件')
        data = path.read_bytes()
        data.decode('utf-8')
    except (OSError, ValueError, RuntimeError) as exc:
        print(f'未检查 {spec}：{exc}')
        return 4
    lines = data.count(b'\n') + int(bool(data) and not data.endswith(b'\n'))
    print(f'{spec}: {lines} 行（阈值 300）')
    if lines > 300:
        print('提醒：请评估是否按独立功能模块拆分；职责内聚时可说明理由后保留。')
    print('仅完成篇幅统计，不代表语义完整或业务验收通过。')
    return 0
