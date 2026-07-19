
.PHONY: quick full manifest papers synthesis

quick:
	python3 -B 03_REPRODUCE/verify_immutable.py --profile quick --workspace /tmp/reverse-hessian-quick --jobs 1

full:
	python3 -B 03_REPRODUCE/verify_immutable.py --profile full --workspace /tmp/reverse-hessian-full --jobs 1

manifest:
	python3 -B 03_REPRODUCE/build_manifest.py

papers:
	bash 01_CANONICAL/reverse_hessian/core/paper/build_pdf.sh
	cd 01_CANONICAL/reverse_hessian/extensions/vp_vnp/paper && latexmk -pdf -interaction=nonstopmode -halt-on-error reverse_hessian_VP_VNP_upgrade.tex

synthesis:
	bash 03_REPRODUCE/build_synthesis_pdf.sh /tmp/reverse-hessian-synthesis
