# TODO PUBLIC REPO: verify execution from repository root and further parameterize file paths if needed.
# =============================================================================
# RF + CART PIPELINE LIMPIO (VERSIÃ“N FINAL)
# Diego NÃºÃ±ez Simms
# =============================================================================

rm(list = ls())
graphics.off()
options(stringsAsFactors = FALSE, scipen = 999)

libs <- c(
  "readr","dplyr","tidyr","stringr","lubridate",
  "randomForest","rpart","rpart.plot",
  "RColorBrewer","magrittr","tibble"
)

for (p in libs) {
  if (!require(p, character.only = TRUE)) {
    install.packages(p)
    library(p, character.only = TRUE)
  }
}

cat("âœ” LibrerÃ­as cargadas\n")

# =============================================================================
# 1. CONFIG
# =============================================================================

DATA_PATH <- file.path("data", "processed", "LEVEL3_FJ_merged_ET_T_WUE.csv")

SET_SEED    <- 2025
TRAIN_PROP  <- 0.75
TOP_N_RF    <- 6
N_TREES_RF  <- 500

theta_wp <- 0.05532005
theta_fc <- 0.064879662

#TARGETS <- c("NEE","ET","E","T")
TARGETS <- c("NEE")
ALLOWED_PREDS <- c(
  "PAR","TA","SWC","P_RAIN","VPD","TS",
  "REW_lab"
)

set.seed(SET_SEED)

# =============================================================================
# 2. CARGA DATOS
# =============================================================================

datos_raw <- read_csv(DATA_PATH, show_col_types = FALSE)

cols_swc <- grep("^SWC_F_.*_1_1$", names(datos_raw), value = TRUE)
cols_ts  <- grep("^TS_F_*_1_1$", names(datos_raw), value = TRUE)

datos2 <- datos_raw %>%
  mutate(
    NEE  = as.numeric(NEE_F2),
    SW_IN = as.numeric(SW_IN_F),
    GPP  = as.numeric(GPP_NT),
    RECO = as.numeric(RECO_NT),
    PAR  = as.numeric(PPFD_SUM),
    ET   = as.numeric(ET_F),
    VPD  = as.numeric(VPD_F)/1000,
    LW_IN= as.numeric(LW_IN_F),
    P_RAIN = as.numeric(P_RAIN),

    SWC = if(length(cols_swc)>0)
      rowMeans(select(., any_of(cols_swc)), na.rm = TRUE) else NA_real_,

    TS  = if(length(cols_ts)>0)
      rowMeans(select(., any_of(cols_ts)), na.rm = TRUE) else NA_real_
  )

# =============================================================================
# 3. REW
# =============================================================================

datos2 <- datos2 %>%
  mutate(
    REW_lab = pmax(0, pmin(1, (SWC - theta_wp) / (theta_fc - theta_wp)))
  )

p10 <- quantile(datos2$SWC, 0.10, na.rm = TRUE)
p90 <- quantile(datos2$SWC, 0.90, na.rm = TRUE)

datos2 <- datos2 %>%
  mutate(
    REW_pct = pmax(0, pmin(1, (SWC - p10)/(p90 - p10)))
  )

# =============================================================================
# 4. RANDOM FOREST
# =============================================================================

rf_topvars <- list()

for (target in TARGETS) {

  df_rf <- datos2 %>%
    select(any_of(c(target, ALLOWED_PREDS))) %>%
    drop_na(all_of(target)) %>%
    select(where(~ sum(!is.na(.x)) > 10))

  if(nrow(df_rf) < 30) next

  df_rf <- df_rf %>%
    mutate(across(-all_of(target),
                  ~ ifelse(is.na(.x), median(.x, na.rm=TRUE), .x)))

  rf <- randomForest(
    x = df_rf %>% select(-all_of(target)),
    y = df_rf[[target]],
    ntree = N_TREES_RF,
    importance = TRUE
  )

  imp <- importance(rf, type=1) %>%
    as.data.frame() %>%
    tibble::rownames_to_column("var") %>%
    arrange(desc(`%IncMSE`))

  rf_topvars[[target]] <- head(imp$var, TOP_N_RF)

  cat("\nðŸŒ² RF:", target, "\n")
  print(imp)
}

# =============================================================================
# 5. DATA PARA CART
# =============================================================================

cart_data <- datos2 %>%
  select(any_of(unique(unlist(c(TARGETS, rf_topvars))))) %>%
  mutate(across(everything(),
                ~ ifelse(is.na(.x), median(.x, na.rm=TRUE), .x))) %>%
  drop_na()

# =============================================================================
# 6. GRID DE PARÃMETROS
# =============================================================================

PARAM_GRID <- list(

  NEE = list(
    list(cp=0.01, minsplit=180, maxdepth=2),
    list(cp=0.01, minsplit=200, maxdepth=3),
    list(cp=0.02, minsplit=10, maxdepth=2),
    list(cp=0.01, minsplit=150,  maxdepth=3)
  ),

  ET = list(
    list(cp=0.01, minsplit=50, maxdepth=3),
    list(cp=0.02, minsplit=80, maxdepth=2),
    list(cp=0.01, minsplit=150, maxdepth=2),
    list(cp=0.005, minsplit=30, maxdepth=2)
  ),

  E = list(
    list(cp=0.01, minsplit=50, maxdepth=2),
    list(cp=0.005, minsplit=30, maxdepth=3),
    list(cp=0.02, minsplit=80, maxdepth=2),
    list(cp=0.01, minsplit=150, maxdepth=3)
  ),

  T = list(
    list(cp=0.01, minsplit=100, maxdepth=3),
    list(cp=0.01, minsplit=120, maxdepth=2),
    list(cp=0.01, minsplit=200, maxdepth=2),
    list(cp=0.005, minsplit=200, maxdepth=2)
  )
)

# =============================================================================
# 7. PALETAS
# =============================================================================

paletas <- list(
  NEE = rev(colorRampPalette(brewer.pal(11,"RdYlGn"))(30)),
  ET  = colorRampPalette(brewer.pal(11,"RdBu"))(30),
  E   = colorRampPalette(brewer.pal(9,"Purples"))(30),
  T   = colorRampPalette(brewer.pal(9,"YlOrRd"))(30)
)

# =============================================================================
# 8. FUNCIÃ“N CART
# =============================================================================

run_cart <- function(target, vars, params) {

  df <- cart_data %>% select(all_of(c(target, vars)))

  idx <- sample(seq_len(nrow(df)), size = floor(TRAIN_PROP*nrow(df)))
  tr <- df[idx,]

  tree <- rpart(
    as.formula(paste(target,"~ .")),
    data = tr,
    method = "anova",
    control = rpart.control(
      cp = params$cp,
      minsplit = params$minsplit,
      maxdepth = params$maxdepth
    )
  )

  cp_min <- tree$cptable[which.min(tree$cptable[,"xerror"]),"CP"]

  prune(tree, cp = cp_min)
}

# =============================================================================
# 9. FUNCIÃ“N PLOT (CON COLORES + PAUSA)
# =============================================================================

plot_cart <- function(tree, target, params, i) {

  titulo <- paste0(
    target,
    " | cp=", params$cp,
    " minsplit=", params$minsplit,
    " depth=", params$maxdepth
  )

  # Plot en VSCode
  rpart.plot(
  tree,
  type = 2,
  extra = 101,
  fallen.leaves = TRUE,
  box.palette = paletas[[target]],
  tweak = 1.1
)
  resp <- readline(prompt = "ENTER = seguir | q = salir: ")
  if (resp == "q") stop("â›” Proceso detenido por el usuario")
}

# =============================================================================
# 10. LOOP FINAL (TARGET â†’ CONFIGS)
# =============================================================================

cart_models <- list()

for (target in names(rf_topvars)) {

  cat("\n=============================\n")
  cat("ðŸŒ³ TARGET:", target, "\n")
  cat("=============================\n")

  param_list <- PARAM_GRID[[target]]

  for (i in seq_along(param_list)) {

    params <- param_list[[i]]

    tree <- run_cart(target, rf_topvars[[target]], params)

    cart_models[[paste0(target,"_",i)]] <- tree

    plot_cart(tree, target, params, i)

    cat("\n--- REGLAS", target, "| config", i, "---\n")
    print(rpart.rules(tree))
  }

  readline(prompt = paste("ðŸš€ TERMINASTE", target, "â†’ ENTER para siguiente"))
}

