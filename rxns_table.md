+--------------------------------------------------------------------------+--------------------+---------+-------------+--------------------------+---------+-------------+
| Description                                                              | Parameter          | Value   | Reference   | Parameter                | Value   | Reference   |
+==========================================================================+====================+=========+=============+==========================+=========+=============+
| Calcium binds to CaM progresively                                        | kon_1_CaCaM        |         |             | koff_1_CaCaM             |         |             |
+--------------------------------------------------------------------------+--------------------+---------+-------------+--------------------------+---------+-------------+
|                                                                          | kon_2_CaCaM        |         |             | koff_2_CaCaM             |         |             |
+--------------------------------------------------------------------------+--------------------+---------+-------------+--------------------------+---------+-------------+
|                                                                          | kon_3_CaCaM        |         |             | koff_3_CaCaM             |         |             |
+--------------------------------------------------------------------------+--------------------+---------+-------------+--------------------------+---------+-------------+
|                                                                          | kon_4_CaCaM        |         |             | koff_4_CaCaM             |         |             |
+--------------------------------------------------------------------------+--------------------+---------+-------------+--------------------------+---------+-------------+
| CaMKII subunits active/inactive flicker                                  | kon_CaMKII_act     |         |             | koff_CaMKII_inact        |         |             |
+--------------------------------------------------------------------------+--------------------+---------+-------------+--------------------------+---------+-------------+
| CaM binds to CaMKII. Saturated CaM_Ca4 binds to CaMKII(T306~0, active~1) | kon_CaM_Ca4_CaMKII |         |             |                          |         |             |
+--------------------------------------------------------------------------+--------------------+---------+-------------+--------------------------+---------+-------------+
| CaM unbinds from CaMKII. Wether CaMKII(T286~P) or CaMKII(T286~0)         |                    |         |             | koff_CaM_Ca4_CaMKII286_P |         |             |
+--------------------------------------------------------------------------+--------------------+---------+-------------+--------------------------+---------+-------------+
|                                                                          |                    |         |             | koff_CaM_Ca4_CaMKII286_0 |         |             |
+--------------------------------------------------------------------------+--------------------+---------+-------------+--------------------------+---------+-------------+
| CaMKII T286 phosphorylation                                              | K_P_CaMKII286      |         |             |                          |         |             |
+--------------------------------------------------------------------------+--------------------+---------+-------------+--------------------------+---------+-------------+
| CaMKII T306 phosphorylation                                              | K_P_CaMKII306      |         |             |                          |         |             |
+--------------------------------------------------------------------------+--------------------+---------+-------------+--------------------------+---------+-------------+
| CaMKII dephosphorylation by PP1                                          | Kcat               |         |             |                          |         |             |
+--------------------------------------------------------------------------+--------------------+---------+-------------+--------------------------+---------+-------------+