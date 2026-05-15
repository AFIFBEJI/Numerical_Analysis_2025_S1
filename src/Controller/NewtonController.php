<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class NewtonController extends AbstractController
{
    #[Route('/newton', name: 'app_newton')]
    public function index(Request $request): Response
    {
        $points = [];
        $coefficients = [];
        $polynomial = '';
        $error = null;
        $chartData = null;
        $submittedData = ['x' => [], 'y' => []];

        if ($request->isMethod('POST')) {
            $xValues = $request->request->all('x');
            $yValues = $request->request->all('y');

            // Sauvegarder les données soumises pour les réafficher
            $submittedData = ['x' => $xValues, 'y' => $yValues];

            if (count($xValues) < 2) {
                $error = "Au moins 2 points sont nécessaires pour l'interpolation.";
            } elseif (count($xValues) !== count(array_unique($xValues))) {
                $error = "Les valeurs de x doivent être toutes différentes.";
            } else {
                $x = [];
                $y = [];
                $originalX = [];
                $originalY = [];

                // Conserver les valeurs exactes saisies pour affichage
                foreach ($xValues as $index => $xVal) {
                    $xTrimmed = trim($xVal);
                    $yTrimmed = trim($yValues[$index]);

                    $originalX[] = $xTrimmed;
                    $originalY[] = $yTrimmed;

                    // Conversion pour calculs seulement
                    $x[] = floatval(str_replace(',', '.', $xTrimmed));
                    $y[] = floatval(str_replace(',', '.', $yTrimmed));
                }

                // Préparer points pour affichage exact
                for ($i = 0; $i < count($x); $i++) {
                    $points[] = ['x' => $originalX[$i], 'y' => $originalY[$i]];
                }

                // CALCUL CORRECT DES DIFFÉRENCES DIVISÉES
                $n = count($x);
                $coefficientsCalc = $this->calculateDividedDifferences($x, $y);

                // Conserver coefficients exacts pour affichage - FORMAT ENTIER
                $coefficients = [];
                foreach ($coefficientsCalc as $c) {
                    $coefficients[] = $this->formatExactNumber($c);
                }

                // POLYNOME DÉVELOPPÉ SEULEMENT
                $polynomial = $this->simplifyPolynomial($coefficientsCalc, $x);

                // Préparer données pour le graphique
                $chartData = $this->prepareChartData($coefficientsCalc, $x, $points);
            }
        }

        return $this->render('newton/index.html.twig', [
            'points' => $points,
            'coefficients' => $coefficients,
            'polynomial' => $polynomial,
            'error' => $error,
            'chartData' => $chartData,
            'submittedData' => $submittedData
        ]);
    }

    /* ========================================================================
       CALCUL CORRECT DES DIFFÉRENCES DIVISÉES
       ======================================================================== */
    private function calculateDividedDifferences(array $x, array $y): array
    {
        $n = count($x);
        $coefficients = [];
        
        // Tableau pour stocker toutes les différences divisées
        $dd = [];
        
        // Initialiser avec les ordonnées (différences divisées d'ordre 0)
        for ($i = 0; $i < $n; $i++) {
            $dd[$i][0] = $y[$i];
        }
        
        // Calculer les différences divisées d'ordre supérieur
        for ($j = 1; $j < $n; $j++) {
            for ($i = 0; $i < $n - $j; $i++) {
                // Formule correcte : f[xi,...,xi+j] = (f[xi+1,...,xi+j] - f[xi,...,xi+j-1]) / (x[i+j] - x[i])
                $dd[$i][$j] = ($dd[$i+1][$j-1] - $dd[$i][$j-1]) / ($x[$i+$j] - $x[$i]);
            }
        }
        
        // Les coefficients sont les premières différences divisées de chaque ordre
        for ($i = 0; $i < $n; $i++) {
            $coefficients[] = $dd[0][$i];
        }
        
        return $coefficients;
    }

    /* ========================================================================
       SIMPLIFICATION DU POLYNÔME (FORME DÉVELOPPÉE) - CORRIGÉE
       ======================================================================== */
    private function simplifyPolynomial(array $coeff, array $x): string
    {
        $n = count($coeff);
        if ($n === 0) return '0';
        
        // Évaluer le polynôme sur plusieurs points pour trouver les coefficients
        // Méthode plus fiable que le développement algébrique
        
        // Créer un système d'équations pour trouver les coefficients
        $degree = $n - 1;
        $A = []; // Matrice des x
        $b = []; // Vecteur des y
        
        // Utiliser n points pour résoudre le système
        for ($i = 0; $i < $n; $i++) {
            $row = [];
            for ($j = 0; $j <= $degree; $j++) {
                $row[] = pow($x[$i], $j);
            }
            $A[] = $row;
            $b[] = $this->evaluateNewtonPolynomial($x[$i], $coeff, $x);
        }
        
        // Résoudre le système linéaire (méthode simple pour petits systèmes)
        $polyCoeffs = $this->solveLinearSystem($A, $b, $degree + 1);
        
        // Construire l'expression simplifiée
        return $this->buildSimplifiedExpression($polyCoeffs);
    }
    
    private function solveLinearSystem(array $A, array $b, int $n): array
    {
        // Méthode d'élimination de Gauss simple
        for ($i = 0; $i < $n; $i++) {
            // Recherche du pivot
            $maxRow = $i;
            for ($k = $i + 1; $k < $n; $k++) {
                if (abs($A[$k][$i]) > abs($A[$maxRow][$i])) {
                    $maxRow = $k;
                }
            }
            
            // Échange des lignes
            if ($maxRow != $i) {
                $temp = $A[$i];
                $A[$i] = $A[$maxRow];
                $A[$maxRow] = $temp;
                $temp = $b[$i];
                $b[$i] = $b[$maxRow];
                $b[$maxRow] = $temp;
            }
            
            // Élimination
            for ($k = $i + 1; $k < $n; $k++) {
                $factor = $A[$k][$i] / $A[$i][$i];
                for ($j = $i; $j < $n; $j++) {
                    $A[$k][$j] -= $factor * $A[$i][$j];
                }
                $b[$k] -= $factor * $b[$i];
            }
        }
        
        // Substitution arrière
        $x = array_fill(0, $n, 0);
        for ($i = $n - 1; $i >= 0; $i--) {
            $sum = 0;
            for ($j = $i + 1; $j < $n; $j++) {
                $sum += $A[$i][$j] * $x[$j];
            }
            $x[$i] = ($b[$i] - $sum) / $A[$i][$i];
        }
        
        return $x;
    }
    
    private function buildSimplifiedExpression(array $coefficients): string
    {
        $n = count($coefficients);
        $expression = "";
        $first = true;
        
        for ($i = $n - 1; $i >= 0; $i--) {
            $coeff = $coefficients[$i];
            if (abs($coeff) < 1e-10) continue;
            
            $coeffFormatted = $this->formatCoefficientForDisplay($coeff);
            
            if ($first) {
                $first = false;
                if ($coeff < 0) {
                    $expression .= "-";
                }
            } else {
                $expression .= $coeff >= 0 ? " + " : " - ";
            }
            
            $absCoeff = abs($coeff);
            $absCoeffFormatted = $this->formatCoefficientForDisplay($absCoeff);
            
            if ($i == 0) {
                $expression .= $absCoeffFormatted;
            } elseif ($i == 1) {
                if ($absCoeffFormatted == "1") {
                    $expression .= "x";
                } else {
                    $expression .= $absCoeffFormatted . "x";
                }
            } else {
                if ($absCoeffFormatted == "1") {
                    $expression .= "x<sup>" . $i . "</sup>";
                } else {
                    $expression .= $absCoeffFormatted . "x<sup>" . $i . "</sup>";
                }
            }
        }
        
        return $expression ?: "0";
    }
    
    private function formatCoefficientForDisplay(float $value): string
    {
        // Si c'est un entier, retourne entier sans décimales
        if (abs($value - round($value)) < 1e-10) {
            return (string) round($value);
        }
        
        // Gestion des fractions communes avec plus de précision
        $tolerance = 1e-8;
        
        // Fractions positives
        if (abs($value - 0.5) < $tolerance) return "1/2";
        if (abs($value - 0.3333333333) < $tolerance) return "1/3";
        if (abs($value - 0.6666666667) < $tolerance) return "2/3";
        if (abs($value - 0.25) < $tolerance) return "1/4";
        if (abs($value - 0.75) < $tolerance) return "3/4";
        if (abs($value - 1.5) < $tolerance) return "3/2";
        
        // Fractions négatives
        if (abs($value + 0.5) < $tolerance) return "1/2";
        if (abs($value + 0.3333333333) < $tolerance) return "1/3";
        if (abs($value + 0.6666666667) < $tolerance) return "2/3";
        if (abs($value + 0.25) < $tolerance) return "1/4";
        if (abs($value + 0.75) < $tolerance) return "3/4";
        if (abs($value + 1.5) < $tolerance) return "3/2";
        
        // Sinon, format décimal
        $formatted = number_format($value, 6, '.', '');
        $formatted = rtrim($formatted, '0');
        $formatted = rtrim($formatted, '.');
        
        return $formatted;
    }

    /* ========================================================================
       AFFICHAGE EXACT: ENTIER SI ENTIER
       ======================================================================== */
    private function formatExactNumber(float $value): string
    {
        // Si c'est un entier, retourne entier sans décimales
        if (abs($value - round($value)) < 1e-10) {
            return (string) round($value);
        }

        // Sinon, affiche avec 6 décimales maximum
        $formatted = number_format($value, 6, '.', '');
        // Supprime les zéros inutiles
        $formatted = rtrim($formatted, '0');
        $formatted = rtrim($formatted, '.');
        
        return $formatted;
    }

    private function prepareChartData(array $coefficients, array $x, array $points): ?array
    {
        if (empty($coefficients)) return null;

        $xValues = array_map(function($p){ return floatval($p['x']); }, $points);
        $minX = min($xValues);
        $maxX = max($xValues);
        $range = $maxX - $minX;

        $extendedMin = $minX - $range * 0.3;
        $extendedMax = $maxX + $range * 0.3;

        $chartX = [];
        $chartY = [];

        for ($i = 0; $i <= 200; $i++) {
            $xi = $extendedMin + ($extendedMax - $extendedMin) * ($i / 200);
            $chartX[] = round($xi, 2);
            $chartY[] = round($this->evaluateNewtonPolynomial($xi, $coefficients, $x), 4);
        }

        return [
            'labels' => $chartX,
            'data' => $chartY,
            'points' => $points,
            'minX' => $extendedMin,
            'maxX' => $extendedMax
        ];
    }

    private function evaluateNewtonPolynomial(float $x, array $coefficients, array $xValues): float
    {
        $result = $coefficients[0];
        $product = 1;

        for ($i = 1; $i < count($coefficients); $i++) {
            $product *= ($x - $xValues[$i - 1]);
            $result += $coefficients[$i] * $product;
        }

        return $result;
    }
}

function gcd($a, $b)
{
    $a = abs($a);
    $b = abs($b);
    return $b == 0 ? $a : gcd($b, $a % $b);
}