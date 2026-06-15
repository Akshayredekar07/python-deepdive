# Python `argparse` 
---

# 1. What is `argparse` and when to use it

`argparse` is the standard library module for parsing command-line arguments in Python. Use it when you want to make scripts configurable from the shell (flags, options, positional args, sub-commands). It handles help messages, type conversion, validation, and usage text automatically.

---

# 2. Basic concepts & minimal example

* **ArgumentParser**: central object that knows how to parse args.
* **add_argument**: declare an argument (positional or option).
* **parse_args()**: parse `sys.argv[1:]` and return a namespace object.

```python
# hello.py
import argparse

def main():
    parser = argparse.ArgumentParser(description="Simple greeter")
    parser.add_argument("name", help="Name to greet")
    parser.add_argument("--times", "-t", type=int, default=1, help="How many times to greet")
    args = parser.parse_args()

    for _ in range(args.times):
        print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()
```

Usage examples:

```
$ python hello.py Alice
Hello, Alice!

$ python hello.py Bob -t 3
Hello, Bob!
Hello, Bob!
Hello, Bob!
```

---

# 3. Argument types & common parameters

`add_argument` parameters you'll use most:

* `name` or `--flag`: positional vs option (dash prefixes make it optional/flag).
* `type`: convert input (`int`, `float`, `str`, custom callable).
* `default`: fallback value.
* `help`: shown in `-h/--help`.
* `required`: True/False (only for optionals).
* `action`: special behaviors (`store_true`, `store_false`, `append`, `count`, or custom).
* `nargs`: number of args expected (`?`, `*`, `+`, `N`, `argparse.REMAINDER`).
* `choices`: restrict allowed values.
* `metavar`: how it shows in usage text.
* `dest`: target attribute name in returned namespace.

Examples:

```python
parser.add_argument('--verbose', '-v', action='count', default=0, help='Increase verbosity')
parser.add_argument('--mode', choices=['train','eval','serve'], required=True)
parser.add_argument('--path', type=str)
parser.add_argument('--threshold', type=float, default=0.5)
parser.add_argument('files', nargs='+', help='Input files (one or more)')
```

`action='count'` increments an integer for repeated `-v` flags. `action='append'` collects multiple values into a list.

---

# 4. Positional vs Optional arguments

* Positional: `parser.add_argument('input')` — required by position.
* Optional: `parser.add_argument('--input')` — can be provided in any order, usually with `--`.

---

# 5. Mutually exclusive groups

Use when options conflict (e.g., `--quiet` vs `--verbose`).

```python
group = parser.add_mutually_exclusive_group()
group.add_argument('-q', '--quiet', action='store_true')
group.add_argument('-v', '--verbose', action='count', default=0)
```

---

# 6. Sub-commands (like `git commit`, `git push`)

Use `add_subparsers()` to create subcommands (each subparser has its own arguments).

```python
# cli_tool.py
import argparse

def cmd_train(args):
    print("Training with", args.epochs, "epochs")

def cmd_eval(args):
    print("Evaluating model at", args.model_path)

def main():
    parser = argparse.ArgumentParser(prog="mltool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train = subparsers.add_parser('train', help="Train a model")
    train.add_argument('--epochs', type=int, default=10)
    train.set_defaults(func=cmd_train)

    eval_p = subparsers.add_parser('eval', help="Evaluate model")
    eval_p.add_argument('model_path')
    eval_p.set_defaults(func=cmd_eval)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
```

Then:

```
$ python cli_tool.py train --epochs 20
Training with 20 epochs
$ python cli_tool.py eval path/to/model.pth
Evaluating model at path/to/model.pth
```

`set_defaults(func=...)` is a convenient dispatch pattern.

---

# 7. Advanced features

## a) Custom types and validation

You can pass a callable to `type` to validate and convert.

```python
def positive_int(x):
    x = int(x)
    if x <= 0:
        raise argparse.ArgumentTypeError("must be > 0")
    return x

parser.add_argument('--batch-size', type=positive_int, default=32)
```

## b) `argparse.FileType`

Open files directly via argparse:

```python
parser.add_argument('input', type=argparse.FileType('r'))
parser.add_argument('--out', type=argparse.FileType('w'), default='-')  # '-' -> stdout
args = parser.parse_args()
text = args.input.read()
```

## c) `parse_known_args`

When you want to accept unknown args (e.g., pass-through to another tool):

```python
known, unknown = parser.parse_known_args()
# known: parsed, unknown: list of unparsed args
```

## d) Custom `Action` classes

For complex behavior when argument appears.

```python
class KeyValueAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        d = getattr(namespace, self.dest, {}) or {}
        key, sep, val = values.partition('=')
        if not sep:
            raise argparse.ArgumentError(self, "must be KEY=VALUE")
        d[key] = val
        setattr(namespace, self.dest, d)

parser.add_argument('--define', action=KeyValueAction, help='Define KEY=VALUE pairs', metavar='KEY=VALUE')
```

## e) `argparse.REMAINDER`

Capture remaining arguments (useful for passing to another program):

```python
parser.add_argument('cmd', nargs=1)
parser.add_argument('cmd_args', nargs=argparse.REMAINDER)
# python mycli.py run -- --flag arg
```

## f) Custom help formatting

Long help messages can be wrapped with different formatters:

```python
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Long description\n  Preserves formatting.")
```

---

# 8. Shell tab-completion (argcomplete)

`argparse` itself doesn't do bash/tab completion, but you can use the `argcomplete` package to provide completion for your argparse apps. Steps (brief):

1. `pip install argcomplete`
2. In your script:

```python
import argcomplete
argcomplete.autocomplete(parser)
```

3. Enable global completion or register a completion for your script (system-dependent).

---

# 9. Integrating config files and environment variables

Common pattern: CLI flags override environment variables, which override config file values, which override defaults.

Example merging logic:

```python
import os
import yaml
import argparse

def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)

parser = argparse.ArgumentParser()
parser.add_argument('--config', help='YAML config file')
parser.add_argument('--lr', type=float)

args = parser.parse_args()
config = {}
if args.config:
    config = load_config(args.config)

def get_setting(name, default=None):
    return getattr(args, name) or os.environ.get(name.upper()) or config.get(name) or default

learning_rate = float(get_setting('lr', 0.001))
```

This approach centralizes precedence.

---

# 10. Using `dataclasses` with argparse

Populate a dataclass from parsed args:

```python
from dataclasses import dataclass
import argparse

@dataclass
class TrainConfig:
    epochs: int = 10
    lr: float = 0.001
    batch_size: int = 32

def parse_args() -> TrainConfig:
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int)
    parser.add_argument('--lr', type=float)
    parser.add_argument('--batch-size', type=int)
    ns = parser.parse_args()
    # Use only provided values to override dataclass defaults
    kwargs = {k: v for k, v in vars(ns).items() if v is not None}
    return TrainConfig(**{**TrainConfig().__dict__, **kwargs})
```

---

# 11. Example: Production-ready CLI for a model project

A multi-subcommand CLI for training, evaluating, and serving — designed for production usage (logging, config precedence, graceful exits, tests).

**Structure**

```
project/
  cli.py
  app/
    __init__.py
    train.py
    evaluate.py
    serve.py
  config/
    default.yaml
```

**cli.py** (complete)

```python
# cli.py
import argparse
import logging
import os
import sys
import yaml
from typing import Dict

LOG = logging.getLogger("myapp")

def load_yaml(path: str) -> Dict:
    if not path:
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}

def setup_logging(verbosity: int):
    level = max(logging.WARNING - (10 * verbosity), logging.DEBUG)
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

def merge_config(cli_ns, env_prefix="MYAPP_", default_config_path="config/default.yaml"):
    config = load_yaml(default_config_path)
    env = {k[len(env_prefix):].lower(): v for k, v in os.environ.items() if k.startswith(env_prefix)}
    # CLI args take highest precedence, then env, then config
    merged = config.copy()
    merged.update(env)
    cli_dict = {k: v for k, v in vars(cli_ns).items() if v is not None}
    merged.update(cli_dict)
    return merged

def main():
    parser = argparse.ArgumentParser(prog="myapp", description="Model training/eval/serve tool")
    parser.add_argument("--config", help="Path to YAML config file")
    parser.add_argument("--verbosity", "-v", action="count", default=0, help="Increase verbosity")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    # train subcommand
    p_train = subparsers.add_parser('train', help='Train model')
    p_train.add_argument('--epochs', type=int, help='Epochs to train')
    p_train.add_argument('--batch-size', type=int, help='Batch size')
    p_train.add_argument('--lr', type=float, help='Learning rate')
    p_train.set_defaults(func='train')

    p_eval = subparsers.add_parser('eval', help='Evaluate model')
    p_eval.add_argument('--model-path', required=True)
    p_eval.set_defaults(func='eval')

    p_serve = subparsers.add_parser('serve', help='Serve model via REST')
    p_serve.add_argument('--port', type=int, default=8080)
    p_serve.set_defaults(func='serve')

    # parse known args to allow passing extra args to subcommands if needed
    args = parser.parse_args()
    setup_logging(args.verbosity)
    LOG.debug("Args parsed: %s", args)

    # Load configs (default file -> env -> CLI)
    if args.config:
        config_path = args.config
    else:
        config_path = "config/default.yaml"  # fallback
    # Merge precedence: default config -> env -> cli
    cfg = merge_config(args, env_prefix="MYAPP_", default_config_path=config_path)
    LOG.debug("Final config: %s", cfg)

    # dispatch
    if args.cmd == 'train':
        from app.train import train
        train(cfg)
    elif args.cmd == 'eval':
        from app.evaluate import evaluate
        evaluate(cfg)
    elif args.cmd == 'serve':
        from app.serve import serve
        serve(cfg)
    else:
        parser.error("Unknown command")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.getLogger("myapp").info("Interrupted by user")
        sys.exit(130)
    except Exception as e:
        logging.getLogger("myapp").exception("Fatal error: %s", e)
        sys.exit(1)
```

**app/train.py** (simplified)

```python
# app/train.py
import logging
LOG = logging.getLogger("myapp.train")

def train(cfg):
    epochs = int(cfg.get('epochs', 10))
    lr = float(cfg.get('lr', 0.001))
    batch_size = int(cfg.get('batch_size', 32))
    LOG.info("Starting training: epochs=%s lr=%s batch_size=%s", epochs, lr, batch_size)
    # Insert training code here (PyTorch / TF)
    # ...
    LOG.info("Training completed")
```

This pattern:

* Central CLI file for parsing and dispatch.
* Per-command modules for functionality (lazy imports inside dispatch to avoid heavy imports on `--help`).
* Config merging function to implement precedence.
* Logging configuration based on `-v`.
* Clean exit codes: `0` on success, `130` for Ctrl-C, `1` for error.

---

# 12. Case study: Batch image processor CLI (complete example)

Goal: create `imgproc` that can resize images, convert formats, and apply operations. Show command, flags, error handling, and tests.

```python
# imgproc.py
import argparse
import logging
import os
from PIL import Image

LOG = logging.getLogger("imgproc")

def resize_image(inpath, outpath, size, overwrite=False):
    if not overwrite and os.path.exists(outpath):
        raise FileExistsError(outpath)
    with Image.open(inpath) as img:
        img = img.resize(size)
        img.save(outpath)
        LOG.info("Saved %s", outpath)

def batch_process(args):
    os.makedirs(args.output, exist_ok=True)
    size = (args.width, args.height)
    for fname in args.inputs:
        base = os.path.basename(fname)
        name, _ = os.path.splitext(base)
        outname = f"{name}.{args.format}"
        outpath = os.path.join(args.output, outname)
        try:
            resize_image(fname, outpath, size, overwrite=args.overwrite)
        except Exception as e:
            LOG.error("Failed %s: %s", fname, e)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="imgproc")
    parser.add_argument('inputs', nargs='+', help='Input image files')
    parser.add_argument('--output', '-o', default='out', help='Output directory')
    parser.add_argument('--width', type=int, default=800)
    parser.add_argument('--height', type=int, default=600)
    parser.add_argument('--format', choices=['jpg','png','webp'], default='jpg')
    parser.add_argument('--overwrite', action='store_true')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    # logging
    level = max(logging.WARNING - 10 * args.verbose, logging.DEBUG)
    logging.basicConfig(level=level)
    batch_process(args)

if __name__ == "__main__":
    main()
```

Usage:

```
$ python imgproc.py images/*.png -o resized --width 400 --height 300 --format webp -v
```

---

# 13. Tests for argparse CLIs (pytest examples)

Test parsing logic and runtime behavior by calling parser or monkeypatching `sys.argv`.

```python
# tests/test_imgproc.py
import sys
from imgproc import build_parser

def test_parser_basic():
    parser = build_parser()
    ns = parser.parse_args(['a.png', 'b.png', '--width', '100'])
    assert ns.width == 100
    assert ns.height == 600  # default
    assert ns.inputs == ['a.png', 'b.png']

def test_help_shows():
    parser = build_parser()
    with pytest.raises(SystemExit) as exc:
        parser.parse_args(['-h'])
    assert exc.value.code == 0
```

Integration-style test: run script with `subprocess.run` and check exit codes and outputs.

---

# 14. CLI design and UX best practices

* Provide good `help` texts; short description in `ArgumentParser(...)`.
* Use `--version` and implement `parser.add_argument('--version', action='version', version='%(prog)s 1.0')`.
* Favor explicit names and short `-h` for help only; avoid ambiguous flags.
* Keep positional arguments simple and predictable.
* Use subcommands for distinct modes of operation.
* Provide sensible defaults and environment/config integration.
* Fail fast with clear error messages and appropriate non-zero exit codes.
* Print progress and logging to stderr; program output to stdout when possible (so users can pipe results).
* Document examples in README and `--help` usage examples if helpful (in long description).
* Keep `--dry-run` support for destructive operations.

---

# 15. Common pitfalls & how to avoid them

* Overloading `-h`: argparse reserves `-h` for help by default. Avoid redefining it.
* Using mutable defaults in `add_argument(..., default=[])`: avoid shared mutable defaults — use `action='append'` or `default=None` then normalize.
* Overly strict parsing when you need pass-through: use `parse_known_args`.
* Assuming order of optionals matters: optionals can appear in any order.
* Not documenting side-effects of flags (e.g., `--force` should document it deletes files).
* Using `nargs='*'` on a positional that follows another positional — ambiguity. Prefer `nargs='+'` if at least one required.

---

# 16. Migration note: when to choose `click` or `typer`

`argparse` is great and available in stdlib. For more sophisticated CLIs with decorators and automatic nice help, consider `click` or `typer`. But `argparse` is widely used and often better for simple scripts without external deps.

---

# 17. Quick reference (cheat sheet)

* `parser.add_argument('file')` — positional
* `parser.add_argument('-o', '--output')` — optional
* `action='store_true'` — flag boolean
* `action='count'` — repeated flags increase integer
* `nargs='+'` — one or more
* `nargs='*'` — zero or more
* `nargs='?'` — optional single value
* `nargs=argparse.REMAINDER` — everything else
* `type=...` — cast/validate
* `choices=[...]` — limit values
* `parse_known_args()` — parse known, get unknown list
* `add_subparsers()` — subcommands

---

# 18. Extra advanced examples

## Example: dynamic subcommands (plugin architecture)

Load commands from entry points or a `plugins/` folder and register them as subparsers.

```python
# main.py snippet
subparsers = parser.add_subparsers(dest='cmd')

# dynamic discovery
for plugin in discover_plugins():  # implement discover_plugins
    p = subparsers.add_parser(plugin.name, help=plugin.help)
    plugin.register_arguments(p)
    p.set_defaults(func=plugin.run)
```

This allows independent modules to add commands.

## Example: nested subcommands (git style)

Subparsers of subparsers — supported but keep usage simple to avoid confusing users.

---

# 19. Final: Full production-like example for your DeepFake detection project

If you want a ready-to-use CLI for your DeepFake workflow (train / eval / infer / serve), here’s a compact but realistic script you can drop into your repo (adapt paths and model code):

```python
# df_cli.py
import argparse
import logging
import sys
from app.train import train
from app.eval import evaluate
from app.infer import infer
from app.serve import serve

LOG = logging.getLogger("df")

def build_parser():
    parser = argparse.ArgumentParser(prog="deepfake", description="DeepFake detection toolkit")
    parser.add_argument("--config", help="Path to YAML config")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    sp = parser.add_subparsers(dest='command', required=True)

    p_train = sp.add_parser('train', help='Train model')
    p_train.add_argument('--data-dir', required=True)
    p_train.add_argument('--epochs', type=int, default=10)
    p_train.add_argument('--batch-size', type=int, default=32)
    p_train.set_defaults(func=train)

    p_eval = sp.add_parser('eval', help='Evaluate')
    p_eval.add_argument('--model', required=True)
    p_eval.set_defaults(func=evaluate)

    p_infer = sp.add_parser('infer', help='Run single inference')
    p_infer.add_argument('--model', required=True)
    p_infer.add_argument('input_file')
    p_infer.set_defaults(func=infer)

    p_serve = sp.add_parser('serve', help='Run REST API')
    p_serve.add_argument('--host', default='0.0.0.0')
    p_serve.add_argument('--port', type=int, default=8080)
    p_serve.set_defaults(func=serve)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    level = max(logging.WARNING - 10*args.verbose, logging.DEBUG)
    logging.basicConfig(level=level, format='%(asctime)s %(levelname)s %(message)s')
    try:
        args.func(args)
    except Exception as e:
        LOG.exception("Command failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

`app/train.py`, `app/eval.py`, `app/infer.py`, and `app/serve.py` implement the domain logic (training loop, metrics, REST endpoints). Keep those modules independent to allow unit testing.

---

# 20. Learning path & practice exercises

1. Start with small scripts (hello.py) — practice `positional`, `--flag`, `--count`.
2. Implement a file converter (e.g., image resize) — practice `FileType`, `nargs`, `--output`.
3. Add subcommands to an existing script (train/eval/serve).
4. Add config file precedence and environment variable integration.
5. Write pytest unit tests for parsing and integration tests for behaviour.
6. Add argcomplete for tab completion when comfortable.

---

# 21. Resources and next steps I can help with

If you want, I can:

* Turn any of the examples above into a GitHub-ready repo structure with tests.
* Provide an extended `train.py` example with PyTorch training loop, checkpointing, and CLI hooks.
* Show how to add `argcomplete` and a packaging `setup.cfg` / `pyproject.toml` entry point for installing CLI as `deepfake` command.
* Show sample `default.yaml` and how to override via env vars.

Tell me which of the above you want next (e.g., a full repo scaffold for your DeepFake project CLI), and I’ll produce the code and tests right away.
