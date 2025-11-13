import unittest
import papermill as pm
import tempfile
from pathlib import Path
import os
import shutil

NOTEBOOK = "tellseq_C_equal_volume_pooling.ipynb"

# Golden files live under notebooks/test_output/<subdir>/<filename>
EXPECTED_SUBDIRS = ["Pooling", "Indices", "SampleSheets", "QC"]

# Only compare data files (skip .ipynb, images, etc.)
DATA_EXTS = {".txt", ".csv", ".tsv"}


class TestTellseqC_ShadowWorkspace(unittest.TestCase):
    def setUp(self):
        # project root (parent of this test file’s folder)
        self.notebooks_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.repo_test_output_dir = os.path.join(self.notebooks_dir, "test_output")

        # sanity: required inputs exist in repo
        must_inputs = [
            os.path.join(self.repo_test_output_dir, "QC", "Tellseq_plate_df_B.txt"),
            os.path.join(self.repo_test_output_dir, "QC", "Tellseq_expt_info.yml"),
        ]
        for fp in must_inputs:
            if not os.path.isfile(fp):
                raise FileNotFoundError(f"[SETUP] Required input not found in repo: {fp}")

    def _find_expected_path(self, filename: str) -> str:
        """Find golden file by filename under test_output/<subdir>/*."""
        for sub in EXPECTED_SUBDIRS:
            candidate = os.path.join(self.repo_test_output_dir, sub, filename)
            if os.path.exists(candidate):
                return candidate
        raise AssertionError(
            f"[COMPARE] Expected golden file not found for '{filename}'. "
            f"Searched under: {', '.join(EXPECTED_SUBDIRS)}"
        )

    def _assert_text_files_equal(self, produced_fp: Path, expected_fp: Path):
        """Strict line-by-line text comparison with helpful diffs."""
        with open(produced_fp, "r") as f_out, open(expected_fp, "r") as f_exp:
            out_lines = f_out.readlines()
            exp_lines = f_exp.readlines()

        self.assertEqual(
            len(out_lines), len(exp_lines),
            msg=(f"[DIFF] Line count differs for '{produced_fp.name}': "
                 f"produced={len(out_lines)} vs expected={len(exp_lines)}")
        )

        for i, (o, e) in enumerate(zip(out_lines, exp_lines), start=1):
            if o != e:
                self.fail(
                    f"[DIFF] Mismatch in '{produced_fp.name}' at line {i}.\n"
                    f"Produced: {o.rstrip()}\n"
                    f"Expected: {e.rstrip()}\n"
                )

    def test_equal_volume_pooling_outputs_shadow(self):
        """
        Keep Notebook C's hardcoded './test_output/...' as-is by creating that
        structure under a temp dir and running with cwd=tmp. Then compare tmp outputs
        vs repo goldens by filename.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)            # shadow root = './'
            tmp_out  = tmp_root / "test_output" # ./test_output
            tmp_qc   = tmp_out / "QC"
            tmp_idx  = tmp_out / "Indices"
            tmp_ss   = tmp_out / "SampleSheets"

            # create expected dirs under tmp
            for d in (tmp_qc, tmp_idx, tmp_ss):
                d.mkdir(parents=True, exist_ok=True)

            # copy required inputs from repo -> tmp
            shutil.copy2(
                os.path.join(self.repo_test_output_dir, "QC", "Tellseq_plate_df_B.txt"),
                tmp_qc / "Tellseq_plate_df_B.txt",
            )
            shutil.copy2(
                os.path.join(self.repo_test_output_dir, "QC", "Tellseq_expt_info.yml"),
                tmp_qc / "Tellseq_expt_info.yml",
            )
     
           
            run_params = {
                "current_set_id": "col19to24",
                "total_vol": 190,
                "iseq_sequencer": "iSeq",
                "novaseq_sequencer": "NovaSeqXPlus",
                "full_plate_fp": "./test_output/QC/Tellseq_plate_df_B.txt",
                "expt_config_fp": "./test_output/QC/Tellseq_expt_info.yml",
            }
    
            # run notebook with cwd switched to tmp_root so './test_output' points to tmp
            prev_cwd = os.getcwd()
            try:
                os.chdir(tmp_root)
                pm.execute_notebook(
                    input_path=os.path.join(self.notebooks_dir, NOTEBOOK),
                    output_path=str(tmp_root / "executed_test_equal_volume_pooling.ipynb"),
                    parameters=run_params,
                    log_output=True,
                )
            finally:
                os.chdir(prev_cwd)

            # collect produced data files under tmp/test_output (skip .ipynb)
            produced_files = [
                p for p in tmp_root.glob("test_output/**/*")
                if p.is_file() and p.suffix.lower() in DATA_EXTS
            ]
            self.assertTrue(
                produced_files,
                msg="[CHECK] No data outputs (.txt/.csv/.tsv) were produced under tmp/test_output."
            )

            # --- Expect exactly the names you observed were produced ---
            expected_names = {
                "Tellseq_evp_set_col19to24.txt",
                "Tellseq_plate_df_B.txt",
                "Tellseq_plate_df_C_set_col19to24.txt",
                "Tellseq_samplesheet_instrument_iseq_set_col19to24.csv",
                "Tellseq_samplesheet_spp_iseq_set_col19to24.csv",
                "Tellseq_samplesheet_spp_novaseqxplus_set_col19to24.csv",
            }

            # helpful once: see what was actually produced
            print("Produced files:", sorted(p.name for p in produced_files))

            produced_names = {p.name for p in produced_files}
            missing = expected_names - produced_names
            extra   = produced_names - expected_names
            self.assertFalse(missing, f"Missing outputs: {sorted(missing)}")
            self.assertFalse(extra,   f"Unexpected outputs: {sorted(extra)}")

            # compare each produced file to its golden
            for name in sorted(expected_names):
                produced_fp = next(p for p in produced_files if p.name == name)
                expected_fp = self._find_expected_path(name)

                # guard: prevent self-compare if paths somehow coincide
                if Path(expected_fp).resolve() == produced_fp.resolve():
                    self.fail(
                        "[GUARD] Produced file path equals expected golden path:\n"
                        f"  {produced_fp}\n"
                        "Ensure notebook wrote into tmp and goldens remain in repo."
                    )

                self._assert_text_files_equal(produced_fp, Path(expected_fp))


if __name__ == "__main__":
    unittest.main()
